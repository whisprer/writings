import copy
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import publish as p


class PublisherTests(unittest.TestCase):
    def setUp(self):
        self.config = p.read_config(p.ROOT/'demo-details.json')
        self.m = p.metadata(self.config, 'engines', p.ROOT)

    def test_all_chapters_and_plates_preserved(self):
        for book in p.BOOKS:
            m = p.metadata(self.config, book, p.ROOT)
            soup = p.prepare(book, m)
            data = json.loads((p.ROOT/'books'/book/'content.json').read_text())
            self.assertEqual([x['id'] for x in soup.select('.chapter')], [x['id'] for x in data['chapters']])
            self.assertEqual(len(soup.select('.plate')), len(data['chapters']))
            original = p.BeautifulSoup((p.ROOT/'books'/book/'template.html').read_text(), 'html.parser')
            for old, new in zip(original.select('.chapter'), soup.select('.chapter')):
                self.assertEqual(str(old), str(new), f'{book}/{old["id"]}: manuscript or plate changed')
            self.assertFalse(soup.select('.blank'))
            self.assertIsNone(soup.find(id='praise'))
            self.assertIsNone(soup.find(id='soon'))

    def test_metadata_is_plain_text(self):
        m = copy.deepcopy(self.m)
        m['author'] = '<script>alert("x")</script> & Author'
        soup = p.prepare('engines', m)
        self.assertFalse(soup.select('script'))
        self.assertIn('&lt;script&gt;', str(soup))
        self.assertIn(m['author'], soup.get_text())

    def test_empty_sections_disappear(self):
        m = copy.deepcopy(self.m)
        for key in ['dedication','biography','acknowledgements']:
            m[key] = []
        soup = p.prepare('engines', m)
        for id in ['dedication','ack','author','soon','praise']:
            self.assertIsNone(soup.find(id=id))
            self.assertFalse(soup.select(f'a[href="#{id}"]'))

    def test_book_override_retains_publisher(self):
        cfg = copy.deepcopy(self.config)
        cfg['books']['engines'] = {'author': 'A Different Author', 'publisher': {'city': 'Cardiff'}}
        m = p.metadata(cfg, 'engines', p.ROOT)
        self.assertEqual(m['publisher']['name'], self.m['publisher']['name'])
        self.assertEqual(m['publisher']['city'], 'Cardiff')
        self.assertEqual(m['author'], 'A Different Author')

    def test_isbn_checksums_and_format_identity(self):
        self.assertTrue(p.valid_isbn('978-0-306-40615-7'))
        self.assertTrue(p.valid_isbn('0-306-40615-2'))
        self.assertFalse(p.valid_isbn('978-0-306-40615-8'))
        self.assertFalse(p.valid_isbn('1234567890128'))
        cfg = copy.deepcopy(self.config)
        cfg['shared']['isbn'] = {'pdf':'9780306406157', 'epub':'9780306406157'}
        with self.assertRaises(ValueError):
            p.metadata(cfg, 'engines', p.ROOT)

    def test_config_typos_and_duplicates_fail(self):
        with self.assertRaises(ValueError):
            p.validate_shape({'publsiher': {}}, p.BASE)
        with self.assertRaises(ValueError):
            p.validate_shape({'copyright_year': True}, p.BASE)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'config.json'
            path.write_text('{"schema_version":1,"schema_version":2}')
            with self.assertRaises(ValueError):
                p.read_config(path)

    def test_missing_image_fails(self):
        cfg = copy.deepcopy(self.config)
        cfg['shared']['publisher']['imprint_image'] = 'missing.png'
        with self.assertRaises(ValueError):
            p.metadata(cfg, 'engines', p.ROOT)

    def test_supplied_optional_matter_replaces_dummy_content(self):
        m = copy.deepcopy(self.m)
        m['endorsements'] = [{'quote':'A real supplied quotation.', 'credit':'Named reviewer'}]
        m['other_titles'] = [{'title':'An actual book', 'description':'Its supplied description.'}]
        soup = p.prepare('engines', m)
        self.assertIn('Named reviewer', soup.find(id='praise').get_text())
        self.assertIn('An actual book', soup.find(id='soon').get_text())
        self.assertNotIn('Placeholder furniture', soup.get_text())
        self.assertNotIn('Stand-in notices', soup.get_text())

    def test_epub_is_rebuilt_and_references_resolve(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)/'book.epub'
            m = copy.deepcopy(self.m)
            m['isbn'] = {'pdf':'9780306406157', 'epub':'9783161484100'}
            soup = p.prepare('engines', m)
            self.assertIn(m['isbn']['pdf'], soup.find(id='copyright').get_text())
            p.render_epub(soup, 'engines', m, target)
            with zipfile.ZipFile(target) as z:
                names = set(z.namelist())
                opf = ET.fromstring(z.read('OEBPS/content.opf'))
                self.assertEqual(opf.find('.//{'+p.DC+'}creator').text, self.m['author'])
                copyright_text = z.read('OEBPS/copyright.xhtml').decode()
                self.assertIn(m['isbn']['epub'], copyright_text)
                self.assertNotIn(m['isbn']['pdf'], copyright_text)
                manifest = opf.find('{'+p.OPF+'}manifest')
                for item in manifest:
                    self.assertIn('OEBPS/'+item.attrib['href'], names)
                for name in names:
                    if not name.endswith('.xhtml'): continue
                    root = ET.fromstring(z.read(name))
                    for node in root.iter():
                        for attr in ['src','href']:
                            if attr in node.attrib:
                                ref = node.attrib[attr].split('#')[0]
                                if ref and '://' not in ref:
                                    self.assertIn('OEBPS/'+ref, names, (name,ref))
                    self.assertNotIn('[Author]', z.read(name).decode())
                    self.assertNotIn('class="blank"', z.read(name).decode())
                self.assertEqual(z.infolist()[0].filename, 'mimetype')
                self.assertEqual(z.infolist()[0].compress_type, zipfile.ZIP_STORED)

    def test_existing_edition_is_protected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, 'already exists'):
                p.build_one('engines', self.m, Path(tmp), None, ['epub'])


if __name__ == '__main__':
    unittest.main()
