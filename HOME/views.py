
from abc import ABC
from django.shortcuts import render
from django.http import HttpResponse, response
from hangul_utils import split_syllables,join_jamos


# ☆베트남어☞한국어 변환하기 프로그램☆

# 자음-초성
cons = {'b':'ㅂ', 'c':'ㄲ','k':'ㄲ','q':'ㄲ', 'd':'ㅈ', 'đ':'ㄷ' ,
    'g':'ㄱ', 'h':'ㅎ',  'l':'ㄹ',  'm':'ㅁ','n':'ㄴ','j':'ㅈ',
    'p':'ㅃ','r':'ㄹ', 's':'ㅅ', 't':'ㄸ' , 'v':'ㅂ', 'x':'ㅆ'}

# 모음-중성
vowels = {'a':'ㅏ','â':'ㅓ','o':'ㅗ','u':'ㅜ','i':'ㅣ','y':'ㅣ','e':'ㅔ','ê':'ㅔ','ư':'ㅡ',
          'iê':'ㅣ어','ie':'ㅣ어','ye':'ㅣ어','yê':'ㅣ어','ia':'ㅣ어','ươ':'ㅡ어','ưo':'ㅡ어','uo':'ㅡ어','ưa':'ㅡ어','uô':'ㅜ어','oi':'ㅗ이','iu':'ㅣ우','ui':'ㅜ이','ai':'ㅏ이',
          'ua':'ㅜ어','ưi':'ㅡ이','ơi':'ㅓ이','ây':'ㅓ이','ai':'ㅏ이','ay':'ㅏ이','oa':'ㅘ','oi':'ㅗ이','êu':'ㅔ우','eo':'ㅐ우','ưu':'ㅓ우',
          'âu':'ㅓ우','ao':'ㅏ어','au':'ㅏ우','uy':'ㅟ','uê':'ㅞ','ue':'ㅜ애','oe':'ㅙ','uơ':'ㅝ','uâ':'ㅝ','oă':'ㅘ',
          'ươi':'ㅡ어이','ưoi':'ㅡ어이','uoi':'ㅡ어이','uôi':'ㅜ어이','uya':'ㅟ어','uyê':'ㅟ어','uye':'ㅟ어','iêu':'ㅣ어우','yêu':'이어우','yeu':'이어우','ươu':'ㅡ어우','uây':'ㅝ이','oai':'ㅘ이',
          'oay':'ㅘ이','uyu':'ㅟ우','oeo':'ㅙ우','oao':'ㅘ우','uay':'ㅜ아이'}

#모음-초성
vowels1 = {'a':'아','â':'아','o':'오','u':'우','i':'이','y':'이','e':'애','ê':'에','ư':'으',
        'iê':'이어','ie':'이어','ye':'이어','yê':'이어','ia':'이어','ươ':'으어','ưo':'으어','uo':'으어','ưa':'으어','uô':'우어','oi':'우이','iu':'이우','ui':'우이','ai':'아이',
          'ua':'워','ưi':'으이','ơi':'어이','ây':'어이','ai':'아이','ay':'아이','oa':'와','oi':'오이','êu':'에우','eo':'애우','ưu':'어우',
          'âu':'어우','ao':'아어','au':'아우','uy':'위','uê':'웨','ue':'우애','oe':'왜','uơ':'워','uâ':'워','oă':'와',
          'ươi':'으어이','ưoi':'으어이','uoi':'으어이','uôi':'워이','uya':'위어','uyê':'위어','uye':'위어','iêu':'이어우','yêu':'이어우','yeu':'이어우','ươu':'으어우','uây':'워이','oai':'와이',
          'oay':'와이','uyu':'위우','oeo':'왜우','oao':'와우','uay':'우아이' }

# 자음-종성
cons_double = {'gi':'ㅈ','ngh':'응','gh':'ㄱ','ph':'ㅍ','nh':'니','ch':'ㅉ','tr':'ㅉ','th':'ㅌ','kh':'ㅋ','ng':'응'}
cons_final = {'ng':'ㅇ', 'ngh':'ㅇ', 'nh':'ㄴ', 'ph':'ㅍ','p':'ㅂ', 'n':'ㄴ', 't':'ㅅ', 'c':'ㄱ', 'k':'ㄱ', 'q':'ㄱ','ch':'ㄱ',
    'm':'ㅁ'}

#베트남의 모음: 영어 모음 
eng_vowels = {
    'à': 'a','á': 'a','ả': 'a','ã': 'a','ạ': 'a','ă': 'a','ắ': 'a','ằ': 'a','ẵ': 'a','ặ': 'a','ẳ': 'a','â': 'a',
    'ầ': 'a','ấ': 'a','ậ': 'a','ẫ': 'a','ẩ': 'a',
    'đ': 'd',
    'è': 'e','é': 'e','ẻ': 'e','ẽ': 'e','ẹ': 'e','ê': 'e','ề': 'e','ế': 'e','ể': 'e','ễ': 'e','ệ': 'e',
    'ì': 'i','í': 'i','ỉ': 'i','ĩ': 'i','ị': 'i',
    'ò': 'o','ó': 'o','ỏ': 'o','õ': 'o','ọ': 'o','ô': 'o','ồ': 'o','ố': 'o','ổ': 'o','ỗ': 'o','ơ': 'o','ờ': 'o','ớ': 'o','ở': 'o','ỡ': 'o','ợ': 'o','ộ':'o',
    'ù': 'u','ú': 'u','ủ': 'u','ũ': 'u','ụ': 'u','ư': 'u','ừ': 'u','ứ': 'u','ử': 'u','ữ': 'u','ự': 'u',
    'ỳ': 'y','ý': 'y','ỷ': 'y','ỹ': 'y','ỵ': 'y'}

#베트남의 모음 성조 빼기
vn_vowel={'à': 'a','á': 'a','ả': 'a','ã': 'a','ạ': 'a','ă': 'a','ắ': 'a','ằ': 'a','ẵ': 'a','ặ': 'a','ẳ': 'a','â': 'â',
    'ầ': 'â','ấ': 'â','ậ': 'â','ẫ': 'â','ẩ': 'â',
    'è': 'e','é': 'e','ẻ': 'e','ẽ': 'e','ẹ': 'e','ê': 'ê','ề': 'ê','ế': 'ê','ể': 'ê','ễ': 'ê','ệ': 'ê',
    'ò': 'o','ó': 'o','ỏ': 'o','õ': 'o','ọ': 'o','ô': 'o','ồ': 'o','ố': 'o','ổ': 'o','ỗ': 'o','ơ': 'o','ờ': 'o','ớ': 'o','ở': 'o','ỡ': 'o','ợ': 'o','ộ':'o',
    'ù': 'u','ú': 'u','ủ': 'u','ũ': 'u','ụ': 'u','ư': 'ư','ừ': 'ư','ứ': 'ư','ử': 'ư','ữ': 'ư','ự': 'ư',
    'đ': 'đ',
    'ì': 'i','í': 'i','ỉ': 'i','ĩ': 'i','ị': 'i',
    'ỳ': 'y','ý': 'y','ỷ': 'y','ỹ': 'y','ỵ': 'y'}

kr_text = []
eng_text = []
def vnlang(request):
    return render(request, 'pages/vnlang.html')
def krlang(request):
    return render(request, 'pages/krlang.html')
def result_KR(request):
    return render(request, 'pages/result_KR.html')
def result_VN(request):
    return render(request, 'pages/result_VN.html')


def vn_kor(text):# 베트남어 -> 한국어
    # 성조 빼기.
    vnName = list(text)
    for c in vnName:
        for key in vn_vowel.keys():
            if(c == key):
                vnName[vnName.index(c)]=vn_vowel[key]
    vnName=''.join(vnName)
    print(vnName)
    vnName=vnName.split()
    print(vnName)
    VNname=''
    for i in range(len(vnName)):
        VNname+='!'
        for t in vnName[i]:
            if t in vnName[i]:
                VNname+=t
        VNname+='! '
    VNname=VNname.split()
    print(VNname)
    # 1. 해당 글자가 자음인지 모음인지 확인
    vc=''
    for i in range(len(vnName)):
        vc+='!'
        for t in (vnName[i]):
        
            if t in cons:
                vc+='c'
            elif t in vowels:
                vc+='v'
            else:
                vc+=t
        vc+='! '
    vc=vc.split()
    print(vc)
    for i in range(len(VNname)):
        # ccv → FFv / cv → fv / cvv → fVV / vv → VV/ VVv → DDD / cc → dd / vc → vC
        vc[i]= vc[i].replace('ccc','TTT').replace('ccv', 'FFv').replace('cv', 'fv').replace('cvv', 'fVV').replace('vv', 'VV').replace('VVv', 'DDD').replace('cc', 'dd').replace('vc', 'vC').replace('Vc', 'vC').replace('!VV','!BB').replace('!vC', '!AC').replace('!vdd', '!Add').replace('!VvC', '!BBC').replace('!DDD', '!EEE').replace('fDDDc', 'fDDDC').replace('!v!', '!A!')
        for k in range(len(vnName[i])):
            if (vc[i][k:k+2]=='FF' )and (VNname[i][k:k+2]=='ng' or VNname[i][k:k+2]=='nh'):
                vc[i]=vc[i].replace('FFDDD', 'FFEEE',1).replace('FFvC','FFAC',1).replace('FFv','FFA',1).replace('FFVV','FFBB',1).replace('FFDDD', 'FFEEE',1)
            elif (vc[i][k:k+3]=='TTT' )and (VNname[i][k:k+3]=='ngh'):
                vc[i]=vc[i].replace('TTTDDD', 'TTTEEE!',1).replace('TTTv','TTTA',1).replace('TTTVV','TTTBB',1).replace('TTTvC','TTTAC',1).replace('TTTDDD', 'TTTSEEE',1)
            elif (vc[i][k:k+2]=='fV' or vc[i][k:k+2]=='fD') and (VNname[i][k:k+2]=='gi'):
                vc[i]=vc[i].replace('fVVC','FFvC',1).replace('fDDD','FFVV',1).replace('fVVdd','FFvdd',1).replace('fVV','FFv',1).replace('fVvC','FFvC',1)
            
            elif (vc[i][k:k+3]=='FFv' or vc[i][k:k+3]=='FFA') and (VNname[i][k:k+3]=='thi'):
                vc[i]=vc[i].replace('FFA','FFv',1)
    print(vc)
    return vn_eng_edit(vc,VNname)
def vn_eng_edit(vc,VNname):# 2. 자음 / 모음 / 두글자 자음 에서 검색
        result = ''   # 영 > 한 변환 결과
        for i in range(len(VNname)):
                k = 0
                while k< len(VNname[i]):
                        v=vc[i][k]
                        t=VNname[i][k]
                        j=1
                        try:
                                if v == 'f' or v == 'c':# 초성(f) & 자음(c) = 자음
                                        result+=cons[t]
                                elif v == 'F':   # 더블 자음-초성
                                        result+=cons_double[VNname[i][k:k+2]]
                                        j+=1
                                elif v == 'C':   # 자음-종성
                                        result+=cons_final[t]
                                elif v == 'v' :   # 모음
                                        result+=vowels[t]
                                elif v == 'V':   # 더블 모음
                                        result+=vowels[VNname[i][k:k+2]]
                                        j+=1
                                elif v == 'd':   # 더블 자음 - 종성
                                        result+=cons_final[VNname[i][k:k+2]]
                                        j+=1
                                elif v == 'D': # 츄플 모음
                                        result+=vowels[VNname[i][k:k+3]]
                                        j+=2
                                elif v == 'A': # 모음-초성
                                        result+=vowels1[t]
                                elif v == 'B': # 더블 모음-초성
                                        result+=vowels1[VNname[i][k:k+2]]
                                        j+=1
                                elif v == 'E': # 츄플 모음 -초성
                                        result+=vowels1[VNname[i][k:k+3]]
                                        j+=2
                                elif v == 'T': # 츄플 자음
                                        result+=cons_double[VNname[i][k:k+3]]
                                        j+=2
                                else:
                                        result+=t

                                # 베트남어나 영어가 아닐 경우
                        except:
                                if v in cons:
                                        result+=cons[t]
                                elif v in vowels:
                                        result+=vowels[t]
                                else:
                                        result+=t
                        k += j
        result=result.replace('!!',' ').replace('!','')
        print(result)
        return join_name(result)
        
        
def vn_eng(List):#베트남어 -> 영어
    name_list = list(List)
    for c in name_list:
        for key in eng_vowels.keys():
            if( c == key):
               name_list[name_list.index(c)]= eng_vowels[key]
    Name_string = ''.join(name_list)           
    Name_string = Name_string.upper()
    return eng_text.append(Name_string)

def join_name(List):
    # pip install hangul-utils
    jamo = split_syllables(List)
    restored_text = join_jamos(jamo)
    return kr_text.append(restored_text)

def CHOICES_KR(request):
    choice=['1','2','3']
    if request.method=='POST':
       choice =request.POST.getlist('choice')
       get_text = request.POST.get('inputtext')
       if choice==['1']:
           text= '영어로 변환하기'
           words = get_text.lower()
           vn_eng(words)        
       if choice==['2']:
           text= '한국어로 변환하기'
           words = get_text.lower()
           vn_kor(words)        
       if choice==['3']:
           text= '영어와 한국어로 다 변환하기'
           words = get_text.lower()
           vn_eng(words)
           vn_kor(words)           
    return render(request,'pages/result_KR.html', {'choice': text, 'input_text': get_text, 'eng_text':eng_text,'kr_text':kr_text})

def CHOICES_VN(request):
    ms=['1','2','3']
    if request.method=='POST':
       choice=request.POST.getlist('choice')
       get_text = request.POST.get('inputtext')
       if choice==['1']: 
           text= 'Đổi sang tiếng anh'
           words = get_text.lower()
           vn_eng(words)          
       if choice==['2']:
           text= 'Đổi sang tiếng hàn'
           words = get_text.lower()
           vn_kor(words)          
       if choice==['3']:
           text= 'Đổi sang cả tiếng anh và tiếng hàn'
           words = get_text.lower()
           vn_eng(words)
           vn_kor(words)         
    return render(request,'pages/result_VN.html', {'choice': text, 'input_text': get_text, 'eng_text':eng_text,'kr_text':kr_text})

def clear_list_KR(request):
    kr_text.clear()
    eng_text.clear()
    return render(request,'pages/krlang.html')

def clear_list_VN(request):
    kr_text.clear()
    eng_text.clear()
    return render(request,'pages/vnlang.html')
