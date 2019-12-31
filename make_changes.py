from collections import defaultdict


text = []
for l in open('iran_list_final.txt','r'):
    text.append(l.strip('\t\n').split('\t'))



change_cat = defaultdict(list)


#change_cat['Cw'] = ['aCwa', 'arSa', 'barzAd', 'bRzant', 'caTwRCat', 'CyAwa', 'daCa', 'g(a)rna-ka', 'hiZwAna', 'muSti', 'parna', 'pRna', 'pRtu', 'vahAra', 'w(a)rda', 'wafra', 'wahuni', 'wahya', 'waicIna?', 'wAr', 'warna-ka', 'wAta', 'wRka', 'wyAka', 'wyAna', 'JRd', 'barda', 'Cwaita', 'Cwaka', 'puTra', 'wara', 'warka', 'wart-', 'wasI', 'wat-caka', 'wata', 'wRpaka', 'gau-cWanta-', 'aCru', 'laupACa', 'p(a)rdanku', 'RZifya', 'viCati', 'waiSa', 'waita', 'wana', 'wanjecaka', 'wRSnaka', 'wRtka', 'WarzI-kAra', 'CwiSa', 'wAz', '(f)SupAna', 'kRmi', 'marZ', 'wAf', 'waina', 'widawA', 'rASta', 'widAna', 'spRzan', 'warAZa', 'wartaka-', 'Carda', 'waCya', 'wrinji', 'darn', 'winACa', 'kaCyapa', 'wagza', 'waZra', 'wicAra', 'wiyapAna', 'Zarnu-mani', 'wRCa-ka- ?', 'waZr(a)ka', 'skar', 'Ciaina', 'wahiSta', 'caxra-', 'xSap', 'xSwifta-']


change_cat['C'] = ['Carda','daCa','laupACa','wiCati','winACa']


change_cat['Cw'] = ['Cwaita', 'Cwaka', 'CwiSa', 'aCwa', 'gau-Cwanta-']


change_cat['Cr'] = ['aCru', 'aCru-ka']


change_cat['Cy'] = ['CyAwa', 'waCya', 'kaCyapa', 'Ciaina']


change_cat['w'] = ['wahAra', 'wiCati', 'w(a)rda', 'wAf', 'wAr', 'wAta', 'wAJi(n)', 'wAJi(yaka?)', 'wRCa-ka-', 'wRSnaka', 'wRka', 'wRpaka', 'wRtka', 'waCya', 'waJr(a)ka', 'waJra', 'wafra', 'wagza', 'wahiSta', 'wahuni', 'wahya', 'waiSa', 'waicIna?', 'waina', 'waita', 'wana', 'wanjecaka', 'warAJa', 'wara', 'warka', 'warna-ka', 'wart-', 'warta-', 'wasI', 'wat-caka', 'wata', 'wicAra', 'widAna', 'widawA', 'winACa', 'wiyapAna', 'wrinji', 'wyAka', 'wyAna']


change_cat['meta'] = ['wafra','caxra-']


change_cat['Jw'] = ['hiJwAna']


change_cat['rs'] = ['arSa','wRSnaka']


change_cat['pro'] = ['arSa','aCru']


change_cat['tr'] = ['puTra']


change_cat['S'] = ['xSap','(f)SupAna']


change_cat['St'] = ['rASta', 'muSti']


change_cat['rn'] = ['pRna','g(a)rna-ka', 'parna', 'warna-ka', 'darn', 'Jarnu-mani',]


change_cat['rJ'] = ['marJ','barzAd', 'warJI-kAra','bRzant', 'spRzan','RJifya']


change_cat['rd'] = ['JRd','w(a)rda', 'barda', 'p(a)rdanku', 'Carda']


change_cat['rt'] = ['pRtu']


change_cat['rC'] = ['caTwRCat', 'wRCa-ka-']


change_cat['r'] = ['skar','kRmi','warka']


change_cat['l'] = ['laupACa']


change_cat['t'] = ['xSwifta-']


assert(sorted(set([v for k in change_cat.keys() for v in change_cat[k]]))==sorted(set([l[0] for l in text])))


used_keys = []
change_list = []
for l in text:
    etym,lang,reflex=l[0],l[2],l[3]
    if etym in change_cat['C']:
        used_keys.append('C')
        if 's' in reflex:
            change_list.append([lang,etym,reflex,'C','s'])
        else:
            change_list.append([lang,etym,reflex,'C','h'])                
    if etym in change_cat['Cw']:
        used_keys.append('Cw')
        if 'p' in reflex or 'f' in reflex or 'b' in reflex or 'm' in reflex:
            change_list.append([lang,etym,reflex,'CW','sp'])
        else:
            change_list.append([lang,etym,reflex,'CW','s'])        
    if etym in change_cat['Cr']:
        used_keys.append('Cr')
        if 'sr' in reflex:
            change_list.append([lang,etym,reflex,'Cr','sr'])
        elif 'rs' in reflex:
            change_list.append([lang,etym,reflex,'Cr','rs'])
        elif 'S' in reflex or 'š' in reflex or 'sh' in reflex:
            change_list.append([lang,etym,reflex,'Cr','S'])        
    if etym in change_cat['Cy']:
        used_keys.append('Cy')
        if 's' in reflex:
            change_list.append([lang,etym,reflex,'CY','s'])
        elif 'S' in reflex or 'š' in reflex:
            change_list.append([lang,etym,reflex,'CY','S'])
    if etym in change_cat['w']:
        used_keys.append('w')
        change_list.append([lang,etym,reflex,'W',reflex.replace('v','w').replace('kh','x')[0]])            
    if etym in change_cat['meta']:
        used_keys.append('meta')
        if 'xr' in reflex or 'fr' in reflex or 'wr' in reflex:
            change_list.append([lang,etym,reflex,'meta','no_meta'])
        elif 'rx' in reflex or 'rf' in reflex or 'rp' in reflex or 'rw' in reflex:
            change_list.append([lang,etym,reflex,'meta','meta'])
        else:
            change_list.append([lang,etym,reflex,'meta','unclear'])
    if etym in change_cat['Jw']:
        used_keys.append('Jw')
        if 'w' in reflex or 'v' in reflex or 'B' in reflex or 'h' in reflex or 'UA' in reflex or 'ua' in reflex:
            change_list.append([lang,etym,reflex,'JW','zw'])
        elif 'm' in reflex:
            change_list.append([lang,etym,reflex,'JW','zm'])
        elif 'b' in reflex:
            change_list.append([lang,etym,reflex,'JW','zb'])
        else:
            change_list.append([lang,etym,reflex,'JW','zw'])
    if etym in change_cat['rs']:
        used_keys.append('rs')
        if 'S' in reflex:
            change_list.append([lang,etym,reflex,'rs','S'])
        elif 'rs' in reflex:
            change_list.append([lang,etym,reflex,'rs','rs'])
        elif 'rch' in reflex:
            change_list.append([lang,etym,reflex,'rs','rch'])
    if etym in change_cat['pro']:
        used_keys.append('pro')
        if reflex.startswith('h') or reflex.startswith('x'):
            change_list.append([lang,etym,reflex,'pro','pro'])
        else:
            change_list.append([lang,etym,reflex,'pro','no_pro'])
    if etym in change_cat['tr']:
        used_keys.append('tr')
        if 's' in reflex:
            change_list.append([lang,etym,reflex,'tr','s'])
        else:
            change_list.append([lang,etym,reflex,'tr','tr'])
    if etym in change_cat['S']:
        used_keys.append('S')
        if reflex.startswith('c'):
            change_list.append([lang,etym,reflex,'S','c'])
        else:
            change_list.append([lang,etym,reflex,'S','S'])
    if etym in change_cat['St']:
        used_keys.append('St')
        if 's' in reflex:
            change_list.append([lang,etym,reflex,'St','st'])
        else:
            change_list.append([lang,etym,reflex,'St','St'])  
    if etym in change_cat['rn']:
        used_keys.append('rn')
        if 'l' in reflex or 'L' in reflex:
            change_list.append([lang,etym,reflex,'rn','l'])
        elif 'n' in reflex:
            change_list.append([lang,etym,reflex,'rn','(r)n'])
        elif 'r' in reflex or 'ř' in reflex:
            change_list.append([lang,etym,reflex,'rn','(r)r'])
    if etym in change_cat['rJ']:
        used_keys.append('rJ')
        if 'l' in reflex or 'L' in reflex:
            change_list.append([lang,etym,reflex,'rJ','l'])
        else:
            change_list.append([lang,etym,reflex,'rJ','rJ'])
    if etym in change_cat['rd']:
        used_keys.append('rd')
        if 'l' in reflex or 'L' in reflex:
            change_list.append([lang,etym,reflex,'rd','l'])
        else:
            change_list.append([lang,etym,reflex,'rd','rd'])
    if etym in change_cat['rt']:
        used_keys.append('rt')
        if 'l' in reflex or 'L' in reflex:
            change_list.append([lang,etym,reflex,'rt','l'])
        else:
            change_list.append([lang,etym,reflex,'rt','rt'])
    if etym in change_cat['rC']:
        used_keys.append('rC')
        if 'l' in reflex or 'L' in reflex:
            change_list.append([lang,etym,reflex,'rC','l'])
        else:
            change_list.append([lang,etym,reflex,'rC','rC'])
    if etym in change_cat['r']:
        used_keys.append('r')
        if 'l' in reflex or 'L' in reflex:
            change_list.append([lang,etym,reflex,'r','l'])
        else:
            change_list.append([lang,etym,reflex,'r','r'])
    if etym in change_cat['l']:
        used_keys.append('l')
        if 'l' in reflex or 'L' in reflex:
            change_list.append([lang,etym,reflex,'l','l'])
        else:
            change_list.append([lang,etym,reflex,'l','r'])
    if etym in change_cat['t']:
        used_keys.append('t')
        if 'r' in reflex:
            change_list.append([lang,etym,reflex,'t','r'])
        else:
            change_list.append([lang,etym,reflex,'t','t'])


assert(sorted(set(used_keys))==sorted(list(change_cat.keys())))
            
            
merge = {'Pahlavi':'Middle Persian',
         'Middle Persian (Manichean)':'Middle Persian',
         'Bakhtiyari_A':'Bakhtiyari',
         'Baxtiyari_Hadank':'Bakhtiyari',
         'Talysh_Schultze':'Talysh',
         'Talysh_Paul':'Talysh'
     }
         


for i in range(len(change_list)):
    if change_list[i][0] in merge.keys():
        change_list[i][0] = merge[change_list[i][0]]


change_list_ = []
for l in change_list:
    if l not in change_list_:
        change_list_.append(l)




replacer    =    """ǰå    \\v{\\j}\\r{a}
$    \\v{s}
o%    \\={o}
@    {\\textschwa}
A    \\={a}
B    {$\\beta$}
C    \\'{c}
D    {$\\delta$}
E    \\={e}
G    {$\\gamma$}
I    \\={i}
J    \\'{\\j}
L    {\\l}
O    \\={o}
R    \\textsubring{r}
S    \\v{s}
T    {\\texttheta}
U    \\={u}
W    \\textsubarch{u}
Y    \\textsubarch{i}
Z    \\v{z}
Á    \\twoacc[\\'|\\={a}]
É    \\twoacc[\\'|\\={e}]
Í    \\twoacc[\\'|\\={\\i}]
Ó    \\twoacc[\\'|\\={o}]
Ö    \\twoacc[\\"|\\={a}]
Ú    \\twoacc[\\'|\\={u}]
Ü    \\twoacc[\\"|\\={a}]
á    \\'{a}
ä    \\"{a}
å    \\r{a}
æ    {\\ae}
ç    \\c{c}
è    \\`{e}
é    \\'{e}
ê    \\^{e}
í    \\'{i}
î    \\^{i}
õ    \\={o}
ö    \\"{o}
ü    \\"{u}
ā    \\={a}
č    \\v{c}
ī    \\={\\i}
ń    \\'{n}
š    \\v{s}
ū    \\={u}
ǧ    \\v{g}
ə    {\\textschwa}
ʕ    {\\IPA Q}
_    \\    
ř    \\={r}
ẓ    \\d{z}
ū́    \\twoacc[\\'|\\={u}]
ō    \\={o}
ń    \\'n
ǧ    \\v{g}
ǻ    \\twoacc[\\'|\\r{a}]
ǰ    \\v{\\j}
ş    \\c{s}"""


replacer = [l.split('    ') for l in replacer.split('\n')]
replace_dict = {l[0]:l[1] for l in replacer}


def convert_to_tex(s):
    for k in replace_dict.keys():
        s=s.replace(k,replace_dict[k])
    return(s)


for i,l in enumerate(change_list):
    change_list[i][0] = change_list[i][0].replace('_',' ')
    change_list[i][1] = change_list[i][1].replace('w','W').replace('y','Y')
    change_list[i][1] = convert_to_tex(change_list[i][1])
    change_list[i][2] = convert_to_tex(change_list[i][2])
    change_list[i][3] = convert_to_tex(change_list[i][3])
    change_list[i][3] = change_list[i][3].replace('_',' ')
    change_list[i][4] = change_list[i][4].replace('_',' ')
    change_list[i][4] = convert_to_tex(change_list[i][4])



f = open('change_list.csv','w')

for l in change_list_:
    print('\t'.join(l),file=f)
    
    
    
f.close()
