"""Poker"""
"""
1. 어떻게 문제에 접근했는가
    나눌 수 있는 만큼 최대한 과업을 나누고, 먼저 수행되야 하는것들을 추려내고 시작했습니다.
    포커 족보에서는 크게 세 유형으로 나눌수 있었는데요, 플러시, 스트레이트, 페어 로 나눠서 생각하고
    높은 점수부터 낮은 점수까지 훑어가다 조건에 맞는 결과를 채택하는게 효율적일거란 생각으로
    로얄플러시를 만들기 위해 필요한 플러시, 스트레이트 부터 함수로 만들었습니다.
    스트레이트 함수를 만들기 위해 정렬이 필요해서 다시 올라가 정렬함수를 만들고, 하는 방식으로
    큰 틀 정도만 잡고 세부적으로 필요한 부분은 마주치면서 해결했습니다.

2. 어떻게 문제를 풀었는가
    어디로 가야될지 모르겠을때 일단 한부분씩 나눠보면서 접근하다보니 조금씩 나아간 것 같습니다.
    그 외에는 종이에 테스트 케이스를 적어보면서 어떻게 하면 내가 원하는 값을 얻을 수 있을지 고민하며 풀었습니다.

3. 생각할 부분
    단순히 코드를 짜는것에만 몰두하는것보다 우선 주어진 문제를 정확하게 이해하는게
    코드를 간결하고 이해하기쉽게 작성하는 데 도움이 되는것 같다고 느꼈습니다.
    특히 마지막에 승부를 결정하는 함수를 작성하면서 많이 배웠습니다.
"""
import os
PATH = os.path.join(os.path.dirname(__file__),"poker.txt")
FILE = open(PATH,"r")
FILE_LIST = FILE.readlines()
FILE.close()

def sorting(card_number_list):
    """ 정렬되지 않은 리스트를 입력하면 오름차순으로 정렬해 반환 """
    while True:
        check = 0 # 다 정렬되었는지 확인하는 변수
        for i in range(4): # 순서대로 정렬되어있는지 확인
            if card_number_list[i] <= card_number_list[i+1]:
                continue
            else:
                card_number_list[i],card_number_list[i+1]=card_number_list[i+1],card_number_list[i]
                # 리스트 내 구성요소 앞뒤로 swap
                check = 1 # 중간에 뒤집었으면 1을 반환해 검사부터 다시 실행
        if check == 0: # 검사결과 모든 값이 순서대로면 While 문 끝남
            break
    return card_number_list # 만든 정렬된 리스트를 반환
#print("Sorting function:",sorting(P1_CDNB_LIST))


def hand_flush(card_list):
    """ Flush 면 1, 아니면 0 반환하는 함수 """
    for i in range(4): # 1,2, 2,3, 3,4, 4,5 가 같은지 확인
        if card_list[i][1]==card_list[i+1][1]:
            continue # 같으면 다음 루프로
        else:
            return 0 # 진행 중 다르면 함수값으로 0 반환
    return 1 # 끝까지 같으면 함수값으로 5 반환
#print("Flush function:",hand_flush(P1_CARD_LIST))


def hand_straight(card_number_list):
    """Straight 면 1, 아니면 0 반환하는 함수"""
    sorted_cn_list = sorting(card_number_list) # 위에서 만든 sorting 함수 활용해 정렬
    check = 0 # 2와 A가 있을때 한번만 넘어가고, 이후 정상적으로 작동하기 위한 변수
    for i in range(4):
        if sorted_cn_list[i]+1 == sorted_cn_list[i+1]: # 이번값+1과 다음값이 동일한지 확인
            continue
        elif sorted_cn_list[0]==2 and sorted_cn_list[-1]==14 and check==0: # 동일하지 않다면 예외상황(A 다음 2)인지 확인
            check = 1 # 예외상황은 한번만 일어나기때문에 다음부터는 예외처리 되지 않게 함
            continue
        else: # 순서대로 1칸씩 차이나게 정렬되지 않았다면 스트레이트가 아님
            return 0 # 스트레이트가 아니니 0을 반환
    return 1 # 스트레이트니 1 반환
#print("Straight function:",hand_straight(P1_CDNB_LIST))


def hand_straightflush(card_list,card_number_list):
    """ StraightFlush면 1, 아니면 0 반환 """
    if(hand_flush(card_list)==1 and hand_straight(card_number_list)==1): # 플러시와 스트레이트를 동시에
        return 1 # 만족시 1 반환
    else:
        return 0 # 불만족시 0 반환
#print("StraightFlush function:",hand_straightflush(P1_CARD_LIST,P1_CDNB_LIST))


def hand_royalflush(card_list,card_number_list):
    """RoyalFlush면 1, 아니면 0 반환"""
    if hand_straightflush(card_list,card_number_list) == 1 and card_number_list[0] == 10:
        # StraightFlush 면서 가장 작은 숫자가 10인 경우 [T, J, Q, K, A] 만 해당됨
        return 1 # 만족시 1 반환
    else:
        return 0 # 불만족시 0 반환
#print("RoyalFlush function:",hand_royalflush(P1_CARD_LIST,P1_CDNB_LIST))


def hand_pairs(card_number_list):
    """Pair 에 따라 다른 값 반환(0,1,2,3,6,7)"""
    sorted_cn_list = sorting(card_number_list) # 위에서 만든 sorting 함수 활용해 정렬
    check_list = [] # 몇번 같았는지 확인하기 위한 변수
    for i in range(4):
        if sorted_cn_list[i] == sorted_cn_list[i+1]: #다음값과 같은지 확인
            check_list.append(1)
        else:
            check_list.append(0)
    #sorted_cn_list -> check_list = [2,2,2,3,3] -> [1,1,0,1]

    check = 0
    if sum(check_list) == 3:
        #앞뒤 같은게 3개면 포카드나 풀하우스기 때문에 check_list 값을 더해서 비교
        for i in range(3):
            if check_list[i] == check_list[i+1]:
                check += 1
            else:
                pass
        if check == 2:
            return 7 #four of a kind
        else:
            return 6 #Full house
    elif sum(check_list) == 2: #앞뒤 같은게 2개면 쓰리카드나 투페어
        for i in range(3):
            if check_list[i] == 1 and check_list[i+1] == 1:
                check += 1
            else:
                pass
        if check == 1:
            return 3 # Three of a kind
        else:
            return 2 # two pair
    elif sum(check_list) == 1: #앞뒤 같은게 1개면 원페어
        return 1 # one pair
    else: # 전부 아니면 하이카드
        return 0 # high card
#print("Pairs:",hand_pairs(P1_CDNB_LIST))


def hand_winner(p1_card_list,p1_cdnb_list,p2_card_list,p2_cdnb_list):
    """핸드 승자를 가려 p1 승리시 1, p2 승리시 0 반환"""
    # 정렬한 값 (Tie 시 활용)
    p1_cdnb_sorted = sorting(p1_cdnb_list)
    p2_cdnb_sorted = sorting(p2_cdnb_list)

    # Check Royal Flush
    p1_score = hand_royalflush(p1_card_list,p1_cdnb_list) # 로얄 플러시면 1, 아니면 0 반환
    p2_score = hand_royalflush(p2_card_list,p2_cdnb_list)
    if p1_score == p2_score:
        pass
    elif p1_score > p2_score:
        return 1 #p1 승리
    else:
        return 0 #p2 승리

    # Check Straight Flush
    p1_score = hand_straightflush(p1_card_list,p1_cdnb_list)
    p2_score = hand_straightflush(p2_card_list,p2_cdnb_list)
    if p1_score == 0 and p2_score==0:
        pass #둘다 해당없는 경우
    elif p1_score > p2_score:
        return 1 #p1 승리
    elif p1_score < p2_score:
        return 0 #p2 승리
    else: #똑같이 스트레이트 플러시인 경우 : Tie Case
        if sorting(p1_cdnb_list)[-1] > sorting(p2_cdnb_list)[-1]:
            return 1 # p1 승리
        else:
            return 0 # p2 승리

    # four of kind, full house, three of kind, two pair, one pair, high card
    p1_score = hand_pairs(p1_cdnb_list) # hand 에 따라 정수 반환
    # straight,flush : hand_pairs 함수에 없는 straight, flush 를 처리
    if p1_score < 4: #Full house 나 four of a kind 가 아니면서
        if hand_straight(p1_cdnb_list)!=0: # 스트레이트 해당되면
            p1_score = 4
        elif hand_flush(p1_card_list)!=0: # 플러시 해당되면
            p1_score = 5
    p2_score = hand_pairs(p2_cdnb_list)
    if p2_score < 4: #Full house 나 four of a kind 가 아니면서
        if hand_straight(p2_cdnb_list)!=0: # 스트레이트 해당되면
            p2_score = 4
        elif hand_flush(p2_card_list)!=0: # 플러시 해당되면
            p2_score = 5

    if p1_score == p2_score: # 두 패의 점수가 같은경우 (하트플러시 vs 클로버플러시 등)
        ### 둘다 포카드 ###
        if p1_score == 7:
            #print("7.Four of a kind - score")
            # 4개의 숫자가 동일함 -> 순서대로 정렬후 가운데 찍으면 무조건 해당되니 서로 비교
            # 포카드 두개가 겹친다 -> 8개 카드의 숫자가 같을수는 없음 -> 크거나 작다만 나옴
            if p1_cdnb_sorted[2] < p2_cdnb_sorted[2]:
                return 0 # 중간값 p2 가 더크면 0 반환
            else:
                return 1 # 중간값 p1 이 더크면 1 반환
        ### 둘다 풀하우스 ###
        elif p1_score == 6:
            #print("6.Full house - score")
            # 쓰리카드를 10의자리, 페어를 1의자리에 둬서 숫자로 비교 하려 했으나
            # 쓰리카드 두개가 겹친다 -> 6개 카드의 숫자가 같을수는 없음 -> 크거나 작다만 나옴
            # 4카드 계산했던것처럼 정렬한 후 가운데 추출하면 3카드 구성요소 추출가능
            if p1_cdnb_sorted[2] < p2_cdnb_sorted[2]:
                return 0 # 중간값 p2 가 더크면 0 반환
            else:
                return 1 # 중간값 p1 이 더크면 1 반환
        ### 둘다 플러시 ###
        elif p1_score == 5:
            #print("5.Flush - score")
            # 순서대로 정렬후 가장 높은카드 뽑고, 동일하면 그다음 계속 비교하는 While True로 비교
            check = -1
            while True: #큰 수부터 서로 대조하며 같으면 반복, 다르면 반복문 종료
                if p1_cdnb_sorted[check] == p2_cdnb_sorted[check]:
                    check -= 1
                    continue
                else:
                    break
            if p1_cdnb_sorted[check] > p2_cdnb_sorted[check]: #반복문 끝난 시점에서 서로 비교
                return 1
            else:
                return 0
        ### 둘다 스트레이트 ###
        elif p1_score == 4:
            #print("4. Straight - score")
            # 순서대로 정렬후 가장 높은값 비교 했을때는 [A 2 3 4 5  A K Q T J]  에서 오류
            # 순서대로 정렬후 가장 높은카드 뽑고, 동일하면 그다음 계속 비교하는 While True로 비교
            check = -1
            while True: #큰 수부터 서로 대조하며 같으면 반복, 다르면 반복문 종료
                if p1_cdnb_sorted[check] == p2_cdnb_sorted[check]:
                    check -= 1
                    continue
                else:
                    break
            if p1_cdnb_sorted[check] > p2_cdnb_sorted[check]: #반복문 끝난 시점에서 서로 비교
                return 1
            else:
                return 0
        elif p1_score == 3: # 둘다 Three of a kind 인 경우
            #print("3.Three of a kind - score")
            # 순서대로 정렬후 첫번째부터 검사하며 세번나온값으로 비교, 이후 높은값 비교
            # 세장끼리 Tie 하는 case는 없음 (3+3=6장이 같은숫자?)
            # 가운데 찝어서 비교
            if p1_cdnb_sorted[2] > p2_cdnb_sorted[2]:
                return 1
            else:
                return 0
        ### 둘다 투페어 ###
        elif p1_score == 2:
            #print("2.Two pair - score")
            # 순서대로 정렬후 첫번째부터 검사하며 두번나온값을 별도 리스트로 만들어 비교, 두개 값 비교 후 하나까지 높은값
            p1_pair_index = []
            p2_pair_index = []
            for i in range(4): # 페어 위치를 먼저 찾음
                if p1_cdnb_sorted[i] == p1_cdnb_sorted[i+1]:
                    p1_pair_index.append(i)
                if p2_cdnb_sorted[i] == p2_cdnb_sorted[i+1]:
                    p2_pair_index.append(i)
            if p1_cdnb_sorted[p1_pair_index[1]] > p2_cdnb_sorted[p2_pair_index[1]]: #큰 페어값이 p1이 더 큰경우
                return 1
            elif p1_cdnb_sorted[p1_pair_index[1]] < p2_cdnb_sorted[p2_pair_index[1]]: #p2가 더 큰경우
                return 0
            else: # 작은 페어값이 동일한 경우
                if p1_cdnb_sorted[p1_pair_index[0]] > p2_cdnb_sorted[p2_pair_index[0]]: #작은 페어값이 p1이 더 큰경우
                    return 1
                elif p1_cdnb_sorted[p1_pair_index[0]] < p2_cdnb_sorted[p2_pair_index[0]]: #p2가 더 큰경우
                    return 0
                else: # 정렬 리스트 - (큰 페어값 + 작은 페어값)
                    p1_cdnb_left = [x for x in p1_cdnb_sorted if x not in p1_cdnb_sorted[p1_pair_index[0]:p1_pair_index[0]+1]+p1_cdnb_sorted[p1_pair_index[1]:p1_pair_index[1]+1]][0]
                    p2_cdnb_left = [x for x in p2_cdnb_sorted if x not in p2_cdnb_sorted[p2_pair_index[0]:p2_pair_index[0]+1]+p2_cdnb_sorted[p2_pair_index[1]:p2_pair_index[1]+1]][0]
                    if p1_cdnb_left > p2_cdnb_left:
                        return 1
                    else:
                        return 0
        ### 둘다 원페어 ###
        elif p1_score == 1:
            #print("1.One pair - score")
            # 순서대로 정렬후 첫번째부터 검사하여 두번나온값이 있으면 뽑아내서 비교, 같으면 해당 값 리스트서 삭제후 크기비교
            p1_pair_index = 0
            p2_pair_index = 0
            for i in range(4): # 페어 위치를 먼저 찾음
                if p1_cdnb_sorted[i] == p1_cdnb_sorted[i+1]:
                    p1_pair_index = i
                if p2_cdnb_sorted[i] == p2_cdnb_sorted[i+1]:
                    p2_pair_index = i
            if p1_cdnb_sorted[p1_pair_index] > p2_cdnb_sorted[p2_pair_index]: # 페어값 p1이 더 큰경우
                return 1
            elif p1_cdnb_sorted[p1_pair_index] < p2_cdnb_sorted[p2_pair_index]: # 페어값 p2가 더 큰경우
                return 0
            else: #서로 같았던 페어를 제외하고 하이카드 계산
                # 정렬된 데이터에서 페어 위치를 차집합하여 페어를 제외한 리스트 추출
                p1_cdnb_left = [x for x in p1_cdnb_sorted if x not in p1_cdnb_sorted[p1_pair_index:p1_pair_index+1]]
                p2_cdnb_left = [x for x in p2_cdnb_sorted if x not in p2_cdnb_sorted[p2_pair_index:p2_pair_index+1]]
                # 순서대로 정렬후 가장 높은값부터 가장 낮은값까지 비교
                check = -1
                while True: #큰 수부터 서로 대조하며 같으면 반복, 다르면 반복문 종료
                    if p1_cdnb_left[check] == p2_cdnb_left[check]: # 리스트 뒤쪽부터 서로 같은지 확인
                        check -= 1
                        continue
                    else:
                        break
                if p1_cdnb_left[check] > p2_cdnb_left[check]: #반복문 끝난 시점에서 서로 비교
                    return 1 #p1이 더 큰경우
                else:
                    return 0 #p2가 더 큰경우
        ### 둘다 하이카드 ###
        elif p1_score == 0:
            #print("0.High card - score")
            # 순서대로 정렬후 가장 높은값부터 가장 낮은값까지 비교
            check = -1
            while True: #큰 수부터 서로 대조하며 같으면 반복, 다르면 반복문 종료
                if p1_cdnb_sorted[check] == p2_cdnb_sorted[check]:
                    check -= 1
                    continue
                else:
                    break
            if p1_cdnb_sorted[check] > p2_cdnb_sorted[check]: #반복문 끝난 시점에서 서로 비교
                return 1
            else:
                return 0

    elif p1_score > p2_score: # p1 점수가 p2 보다 높으면
        return 1 # 플레이어 1 승리
    elif p1_score < p2_score: # p1 점수가 p2 보다 작으면
        return 0 # 플레이어 2 승리
    else:
        print("ERR") #위에서 처리하지 못한 에러 케이스

P1_WIN_COUNT = 0
P2_WIN_COUNT = 0

for TEXT in FILE_LIST:
    TEXT_ROW = TEXT[:-1]+" "  # 줄바꿈문자 제거
    #TEXT_ROW = "KS KD JH JS QC 2C KH KS JD JC"+" "
    CARD_LIST = []
    TEXT = []
    for W in TEXT_ROW: # TEXT_ROW 의 W(Word) 뜯어서 리스트로 만듬 [KS,KD,JH...] -> CARD_LIST
        if W!=" ":
            TEXT += W
        else:
            CARD_LIST.append(TEXT)
            TEXT = []

    CARD_NUMBER_LIST = []
    for I in range(10): # 숫자 값만 따로 뺀 리스트 생성(CARD_NUMBER_LIST)
        CARD_NUMBER_STR = CARD_LIST[I][0]
        try: # int 적용되면 바로 append
            CARD_NUMBER_LIST.append(int(CARD_NUMBER_STR))
        except ValueError: # int 적용안되면 숫자부여후 append
            if CARD_NUMBER_STR == "T":
                CARD_NUMBER_STR = 10
            elif CARD_NUMBER_STR == "J":
                CARD_NUMBER_STR = 11
            elif CARD_NUMBER_STR == "Q":
                CARD_NUMBER_STR = 12
            elif CARD_NUMBER_STR == "K":
                CARD_NUMBER_STR = 13
            else: # "A"
                CARD_NUMBER_STR = 14
            CARD_NUMBER_LIST.append(int(CARD_NUMBER_STR))

    P1_CARD_LIST = CARD_LIST[:5]
    P2_CARD_LIST = CARD_LIST[5:]
    P1_CDNB_LIST = CARD_NUMBER_LIST[:5]
    P2_CDNB_LIST = CARD_NUMBER_LIST[5:]

    #print(P1_CARD_LIST,P1_CDNB_LIST)
    #print(P2_CARD_LIST,P2_CDNB_LIST)

    ### P1 승리시 1, P2 승리시 2 반환 ###
    WINNER = hand_winner(P1_CARD_LIST,P1_CDNB_LIST,P2_CARD_LIST,P2_CDNB_LIST) 
    if WINNER == 1:
        P1_WIN_COUNT += 1
        #print("P1 WIN\n")
    else:
        P2_WIN_COUNT += 1
        #print("P2 WIN\n")

print(P1_WIN_COUNT)#,P2_WIN_COUNT)
