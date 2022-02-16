from ipware import get_client_ip



def extract_ip(req):
        client_ip, is_routable = get_client_ip(req)
        if client_ip is None:
                print("client ip is not found")
                return False
        else:
                if client_ip in whitelist:
                        print(client_ip)
                        return True                        
