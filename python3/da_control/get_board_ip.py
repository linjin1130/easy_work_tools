list1 = 'ABCDEFGHIJKLMN'
list2 = [1,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
list3 = [0,100,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
seg_dic = dict(zip(list1[:10], list(zip(list2[:10], list3[:10]))))
# print(seg_dic)

#根据板号获取IP地址
def get_ip(str_in):
    return '10.0.'+str(seg_dic[str_in[0]][0])+'.'+str(seg_dic[str_in[0]][1] + int(str_in[1:]))+''

def get_ip_list(board_list):
    ip_list = []
    for bd in board_list:
        ip_list.append(get_ip(bd))
    return ip_list

if __name__ == '__main__':
    da_board_list1 = ['C05', 'D13', 'D09', 'D17', 'D01']
    da_board_list2 = ['E09', 'E08', 'E30', 'E26', 'E31']
    da_board_list3 = ['E24','E14','E29','D21','C11','B08','B05','D16','E03','E32','E11','D15','E06']
    da_board_list4 = ['E10','C08','C03','E16','E17','E18','E19','D08','D02','E12','E13','C09','E07','D05','D06','E04']
    ips = get_ip_list(da_board_list1)
    print(ips)