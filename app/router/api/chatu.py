from fastapi import APIRouter, Response, status
import httpx

client = httpx.AsyncClient()

router = APIRouter(tags=["Proxy"])

@router.get("/proxy-chat", status_code=status.HTTP_200_OK)
@router.post("/proxy-chat", status_code=status.HTTP_200_OK)
async def proxy_chat(
        response: Response,
        q: str = "write"
) -> dict:
    """
    Proxy server to handle chat requests and pass it to the target server.
    """
    # 请求目标 URL
    target_url = f"https://mydiumtify.globeapp.dev/chattext?q={q}"
    
    try:
        # 向目标服务器发起请求
        target_response = await client.request(
            method="GET", 
            url=target_url, 
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"
            }
        )
        
        # 检查目标服务器响应状态码
        if target_response.status_code != httpx.codes.OK:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {
                "success": False,
                "data": None,
                "error_message": "A problem occurred on the target server"
            }

        # 将目标服务器的响应转发给客户端
        response_data = target_response.json()
        return {
            "success": True,
            "data": response_data,
            "error_message": None
        }
    
    except Exception as e:
        # 处理请求时的异常
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "success": False,
            "data": None,
            "error_message": f"An error occurred: {e}"
        }
