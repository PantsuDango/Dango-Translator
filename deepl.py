import requests
import time


class DeepLTranslate():

    def __init__(self):
        self.headers = {
                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
                        "cookie": "_ga=GA1.2.722545162.1587439036; LMTBID=v2|e8a259ac-32d4-47e0-85ef-06c749f3c4b2|c2964b04571386fee9bf5bfc1d8a76e4"
                        }
        self.url = "https://www2.deepl.com/jsonrpc"
        self.form_data = {
            "id": 0,
            "jsonrpc": "2.0",
            "method": "LMT_handle_jobs",
            "params": {
                       "commonJobParams": {},
                       "jobs": [{
                                 "kind": "default",
                                 "preferred_num_beams": 4,
                                 "raw_en_context_after": [],
                                 "raw_en_context_before": [],
                                 "raw_en_sentence": "ごめんなさい"
                               }],
                       "lang": {
                                "source_lang_user_selected": "auto",
                                "target_lang": "ZH",
                                "user_preferred_langs": ["EN", "ZH", "JA"]
                               },
                       "priority": 1,
                       "timestamp": int(time.time())
                      }
        }


    def respone(self):
        res = requests.get(self.url, headers=self.headers, data=self.form_data)
        self.html = res.text
        print(self.html)


    def regex(self):
        pass


    def main(self):
        self.respone()


if __name__ == "__main__":
    DeepL = DeepLTranslate()
    DeepL.main()