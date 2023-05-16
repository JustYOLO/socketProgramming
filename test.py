def is_ip(ip: str):
    '''
    주어진 str(ip)이 IPv4 형식인지 확인하는 함수
    return: boolean
    '''
    try:
        nums = list(map(int, ip.split('.')))
    except ValueError:
        print("IP string format is not valid")
        return False
    if len(nums) != 4:
        return False
    for num in nums:
        if num < 0 or num > 255:
            return False
    return True

ip = "1.1.1"

if is_ip(ip):
    print("given input is a ipv4 format")