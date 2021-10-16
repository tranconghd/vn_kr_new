from django.shortcuts import render
from django.http import HttpResponse, response

# Create your views here.
def krlang(request):
    return render(request, 'pages/krlang.html')
def vnlang(request):
    return render(request, 'pages/vnlang.html')
def result_VN(request):
    return render(request, 'pages/result_VN.html')
def result_KR(request):
    return render(request, 'pages/result_KR.html')
def vn_kor(text):# 베트남어 -> 한국어
    # 성조 빼기.
    vnName = list(text)
    for c in vnName:
        for key in vn_vowel.keys():
            if(c == key):
                vnName[vnName.index(c)]=vn_vowel[key]
    vnName=''.join(vnName)
    vnName=vnName.split()
    VNname=''
    for i in range(len(vnName)):
        VNname+='!'
        for t in vnName[i]:
            if t in vnName[i]:
                VNname+=t
        VNname+='! '
    VNname=VNname.split()
   
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
    vn_eng_edit(vc,VNname)
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
        return join_name(result)
        
        
def vn_eng(List):#베트남어 -> 영어
    name_list = list(List)
    for c in name_list:
        for key in eng_vowels.keys():
            if( c == key):
               name_list[name_list.index(c)]= eng_vowels[key]
    Name_string = ''.join(name_list)            
    print(Name_string.upper())

def join_name(List):
    # pip install hangul-utils
    from hangul_utils import split_syllables,join_jamos
    jamo = split_syllables(List)
    restored_text = join_jamos(jamo)
    print(restored_text, end='')