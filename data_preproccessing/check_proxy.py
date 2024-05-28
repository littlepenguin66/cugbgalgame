"""
代理检查模块 - 用于验证代理服务器的状态和位置

这个模块包含两个函数，用于检查代理服务器的有效性，并返回代理的地理位置信息。

函数说明：
_check_with_backup_source(proxies):
- 这是一个辅助函数，用于在主检查失败时作为备份。
- 它尝试通过代理发送HTTP请求到"http://ip-api.com/json"，并解析返回的国家信息。
- 如果成功，返回国家名称；否则，返回None。

check_proxy(proxies):
- 这是主函数，用于检查给定的代理配置。
- 如果代理参数为None，直接返回"没有使用代理"。
- 通过代理发送HTTP请求到"https://ipapi.co/json/"，并解析返回的数据。
- 根据返回的数据，判断代理的有效性和地理位置。
- 如果请求成功，但数据中没有国家名称，尝试使用备份源。
- 如果备份源也失败，或者返回错误，返回相应的错误信息。
- 如果请求超时或发生异常，返回代理可能无效的信息。

使用方法：
1. 导入check_proxy函数。
2. 调用check_proxy函数，传入代理配置字典作为参数。
3. 函数将返回代理的状态和位置信息。

注意：
- 该模块依赖于requests库来发送HTTP请求。
- 代理配置应该是一个字典，包含'https'键，值为代理URL。
- 该模块主要用于开发和测试环境，以验证代理服务器的可用性。
"""
def _check_with_backup_source(proxies):
    import requests
    try:
        response = requests.get("http://ip-api.com/json", proxies=proxies, timeout=4)
        data = response.json()
        if 'country' in data:
            return data['country']
        else:
            return None
    except:
        return None

def check_proxy(proxies):
    import requests
    if proxies is None:
        return "没有使用代理"
    proxies_https = proxies['https']
    try:
        response = requests.get("https://ipapi.co/json/", proxies=proxies, timeout=4)
        data = response.json()
        if 'country_name' in data:
            country = data['country_name']
            result = f"代理配置 {proxies_https}, 代理所在地：{country}"
        elif 'error' in data:
            alternative = _check_with_backup_source(proxies)
            if alternative is None:
                result = f"代理配置 {proxies_https}, 代理所在地：未知，IP查询频率受限"
            else:
                result = f"代理配置 {proxies_https}, 代理所在地：{alternative}"
        else:
            result = f"代理配置 {proxies_https}, 代理数据解析失败：{data}"
        return result
    except:
        result = f"代理配置 {proxies_https}, 代理所在地查询超时，代理可能无效"
        return result

if __name__ == "__main__":
    check_proxy(proxies=None)