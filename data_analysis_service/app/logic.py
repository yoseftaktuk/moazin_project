import base64
from logger.logger import Logger
class DataAnalysisService:
    def decoding_the_information(self):
        bad_to_israel ="R2Vub2NpZGUsV2FyIENyaW1lcyxBcGFydGhlaWQsTWFzc2FjcmUsTmFrYmEsRGlzcGxhY2VtZW50LEh1bWFuaXRhcmlhbiBDcmlzaXMsQmxvY2thZGUsT2NjdXBhdGlvbixSZWZ1Z2VlcyxJQ0MsQkRT"
        lest_bad_for_israel = 'RnJlZWRvbSBGbG90aWxsYSxSZXNpc3RhbmNlLExpYmVyYXRpb24sRnJlZSBQYWxlc3RpbmUsR2F6YSxDZWFzZWZpcmUsUHJvdGVzdCxVTlJXQQ=='
        base64_bytes = bad_to_israel.encode("utf-8")
        bad_to_israel = base64.b64decode(base64_bytes)
        bad_to_israel = bad_to_israel.decode("utf-8").lower()
        lest_bad_for_israel = lest_bad_for_israel.encode('utf-8')
        lest_bad_for_israel = base64.b64decode(lest_bad_for_israel)
        lest_bad_for_israel = lest_bad_for_israel.decode('utf-8').lower()
        return {'lest_bad_for_israel':lest_bad_for_israel.split(','), 'bad_to_israel': bad_to_israel.split(',')}
    
    def content_classification(self, data: dict):
        fix_text = self.fix_the_text(data['string'])
        data['bds_threat_level'] = 'NONE'
        lest_bad_for_israel = self.decoding_the_information()['lest_bad_for_israel']
        bad_to_israel = self.decoding_the_information()['bad_to_israel']
        for word in fix_text:
            if word.lower() in lest_bad_for_israel:
                data['bds_threat_level'] = 'MEDIUM'
                continue
            elif word.lower() in bad_to_israel:
                data['bds_threat_level'] = 'HIGH'
                return data
        return data    
  

    def fix_the_text(self, text: str):
        text = text.split()
        dabel_word = {'freedom':'flotilla', 'humanitarian':'crisis', 'war': 'crimes'}
        new_list = []
        len_text = len(text)
        for i in range(len_text): 
            if text[i].lower() in dabel_word.keys():
                try:
                    if text[i + 1].lower() == dabel_word[text[i]].lower():
                       new_list.append(text[i] + f' {dabel_word[text[i]]}')
                       text[i] += f' {dabel_word[text[i]]}'
                       continue
                except IndexError as e:
                    continue
            if text[i] not in dabel_word.values():         
                new_list.append(text[i])
        return new_list
    
    def get_danger_in_percentage(self, data: dict):#Checks how many bad words there are in relation to the total number of words 
        counter = 0
        fix_text = self.fix_the_text(data['string'])
        lest_bad_for_israel = self.decoding_the_information()['lest_bad_for_israel']
        bad_to_israel = self.decoding_the_information()['bad_to_israel']
        for word in fix_text:
            if word.lower() in lest_bad_for_israel or word.lower() in bad_to_israel:
                counter += 1
        data['bds_percent'] = counter / len(fix_text) * 100       

    def checking_indicted(self, data: dict):
        if data['bds_percent'] >= 5 and data['bds_threat_level'] == 'HIGH':
            data['is_bds'] = True
            return data
        data['is_bds'] = False
        return data
    
    def processing_the_information(self, data: dict):
        self.content_classification(data=data)
        self.get_danger_in_percentage(data=data)
        self.checking_indicted(data=data)
        return data

