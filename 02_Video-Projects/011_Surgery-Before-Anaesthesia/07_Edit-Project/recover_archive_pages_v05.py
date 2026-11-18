"""Extract identified archive pages without network or media generation.

Requires PyMuPDF. Inputs remain untouched; output must be a new directory.
Page indices are one-based PDF pages, not printed folio numbers.
"""
import argparse, hashlib, json
from pathlib import Path
import pymupdf

def sha(path):
    digest=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):digest.update(block)
    return digest.hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--cache',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    args.out.mkdir(parents=True,exist_ok=False)
    manifest=json.loads((args.cache/'ASSEMBLY_SOURCES_v01.json').read_text())
    assets={r['asset_id']:r for r in manifest['assets']}
    result={'job':'J2563','scope':'archive source recovery only; no composite renders or film-stage approval','network':'Original approved Morton and Ether Dome files recovered; subsequent Ether Monument request returned HTTP 429. No further requests.','audio_review':False,'motion_review':False,'sources':[],'page_extracts':[]}
    selected=['archive_P1_09b','archive_P2_04a_arch_davy_1800','archive_P2_05a_arch_laughing_gas_broadside','archive_P2_09b_arch_long_1849','archive_P3_05b','archive_P3_09a_arch_ether_dome_1847']
    for key in selected:
        r=assets[key];src=Path(r['local_file']);assert sha(src)==r['file_sha256'],key
        # Raw external metadata remains outside the public repository.
        result['sources'].append({'asset_id':key,'row_id':r['row_id'],'page_url':r['page_url'],'file_name':src.name,'sha256':sha(src),'bytes':src.stat().st_size,'licence':r['observed_licence']['LicenseShortName'],'credit':r['credit'],'depicts':r.get('depicts'),'status':'identity and layout inspected in stills; composite unbuilt'})
    selections=[('archive_P2_04a_arch_davy_1800',584,'556','Davy 1800: physical pain and surgical operations'),('archive_P2_09b_arch_long_1849',711,None,'December 1849 heading and Long article start; March 1842 in first page'),('archive_P2_09b_arch_long_1849',712,'706','Long article continuation; no publication before December 1849 implied')]
    for key,number,folio,description in selections:
        src=Path(assets[key]['local_file']);doc=pymupdf.open(src);page=doc[number-1]
        text=page.get_text()
        if folio is not None:assert folio in text[:80],(key,number,text[:80])
        else:assert 'DECEMBER' in text[:100] and '1849' in text[:100]
        target=args.out/(key+'_pdf_page_'+str(number)+'.png');pix=page.get_pixmap(matrix=pymupdf.Matrix(3,3),alpha=False);pix.save(target)
        txt=target.with_suffix('.txt');txt.write_text(text)
        result['page_extracts'].append({'asset_id':key,'pdf_page_1based':number,'printed_page':folio,'description':description,'file_name':target.name,'sha256':sha(target),'width':pix.width,'height':pix.height,'extracted_text_file':txt.name,'text_sha256':sha(txt),'source_pdf_sha256':sha(src),'verification':'Printed page and relevant passage visually inspected; OCR is discovery evidence only, not an exact-quote authority.'})
    (args.out/'ARCHIVE_RECOVERY_v05.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print('PASS: six cached source hashes match; three identified PDF pages extracted with source hashes, one-based page numbers and printed folios. Source recovery only; no film-stage PASS.')
if __name__=='__main__':main()
