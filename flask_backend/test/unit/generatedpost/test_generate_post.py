from os import getenv
import responses
import pytest
from pytest_httpx import HTTPXMock

@responses.activate
def test_generate_post(client, auth, public_official_actions, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
            method=responses.POST,
            url="https://api.anthropic.com/v1/messages",
            status_code=200,
            headers={"x-api-key" : getenv("ANTHROPIC_API_KEY")},
            json=
            {
                "content": [
                    {
                    "text": "<title>ג'ף הבחור</title><content>ג'ף אחלה של בחור.</content>",
                    "type": "text"
                    }
                ],
                "id": "msg_013Zva2CMHLNnXjNJJKqJ2EF",
                "model": "claude-3-5-sonnet-20240620",
                "role": "assistant",
                "stop_reason": "stop_sequence",
                "stop_sequence": "[GENERATION_SUCCESSFUL]",
                "type": "message",
                "usage": {
                    "input_tokens": 10,
                    "output_tokens": 25
                }
            }
        )

        # Test Post Generation
    public_official_id = public_official_actions.create_public_official().get_id()

    prompt_dict = {"generation_prompt": "תכין לי פוסט לכבוד יום ההולדת של ג'ף.", 
                "public_official_id": public_official_id, 
                "social_media": "facebook"}

    auth.create_basic_user()

    response = client.post("/post-generation/generate", json=prompt_dict, headers=auth.get_auth_header())
    

    assert response.status_code == 200
    assert response.json["generated_post"]["title"] == "ג'ף הבחור"
    assert response.json["generated_post"]["text"] == "ג'ף אחלה של בחור."

    assert response.json["generated_post"]["user_id"] == auth.get_user_id()
    assert response.json["generated_post"]["public_official_id"] == public_official_id
    
def test_generate_post_with_invalid_public_official_id(client, auth):
    # Test Post Generation with an invalid public_official_id
    prompt_dict = {"generation_prompt": "Make a post about Jeff.", 
                   "public_official_id": "666e3cdc77f6b009eab6d345", #invalid
                   "social_media": "facebook"} 
             
    auth.create_basic_user()

    response = client.post("/post-generation/generate", json=prompt_dict, headers=auth.get_auth_header())

    assert response.status_code == 404

def test_generate_post_with_empty_prompt(client, auth, public_official_actions):
    public_official_id = public_official_actions.create_public_official().get_id()

    prompt_dict = {"generation_prompt": "", 
                   "public_official_id": public_official_id, 
                   "social_media": "facebook"}

    auth.create_basic_user()

    response = client.post("/post-generation/generate", json=prompt_dict, headers=auth.get_auth_header())

    assert response.status_code == 400

def test_generate_post_with_invalid_social_media(client, auth, public_official_actions):
    public_official_id = public_official_actions.create_public_official().get_id()

    prompt_dict = {"generation_prompt": "Make a post about Jeff.", 
                   "public_official_id": public_official_id, 
                   "social_media": "test"} #invalid

    auth.create_basic_user()

    response = client.post("/post-generation/generate", json=prompt_dict, headers=auth.get_auth_header())

    assert response.status_code == 400