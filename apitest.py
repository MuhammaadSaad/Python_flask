import unittest
import requests
from datetime import datetime
# if __name__ == '__main__':
#     unittest.main()


class ApiTest(unittest.TestCase):
    API_URL = "http://127.0.0.1:5000"
    Create_URL = "{}/create".format(API_URL)
    update_URL = "{}/update/{}".format(API_URL,"song")
    delete_url = "{}/delete".format(API_URL)
    songS_URL = "{}/get/{}".format(API_URL,"song")
    podcast_URL = "{}/get/{}".format(API_URL,"podcast")
    audiobook_URL = "{}/get/{}".format(API_URL,"audiobook")
    Songobj={
        "Duration": "175", 
        "Name": "Groove", 
        "Uploaded_time": "2021-03-01 22:21:17.368160"
    }
    
    uSongobj={
        "Duration": "180", 
        "Name": "Groove mera", 
        "Uploaded_time": "2021-03-01 08:48:17.771112"
    }
    updateSongobj={
        "Duration": "180", 
        "Name": "Groove mera"
    }
    NewSongobj= {
    "audioFileType":"song",
    "audioFileMetadata" :{
            
            "Name":"Groove Mera",
            "Duration": 185
            
        }
    }
    NewPodcastobj= {
    "audioFileType":"Podcast",
    "audioFileMetadata" :{
            
            "Name":"Groove Mera",
            "Duration": 185,
            "Host":"HBL PSL",
            "Participants":"Isb,Quetta"
            
        }
    }
    Newaudiobookobj= {
    "audioFileType":"audiobook",
    "audioFileMetadata" :{
            
            "Title":"Groove Mera",
            "Host":"HBL PSL",
            "Author":"HBL PSL",
            "Narrator":"HBL PSL",
            "Duration": 185
            
        }
    }

    def _get_each_song_url(self, song_id):
        return "{}/{}".format(ApiTest.songS_URL, song_id)

    # GET request to /song returns the details of all songs
    def test_1_get_all_songs(self):
        r = requests.get(ApiTest.songS_URL)
        self.assertEqual(r.status_code, 200)
        #self.assertEqual(len(r.json()), 6)
    def test_1_get_all_podcast(self):
        r = requests.get(ApiTest.podcast_URL)
        self.assertEqual(r.status_code, 200)

    def test_1_get_all_audiobooks(self):
        r = requests.get(ApiTest.audiobook_URL)
        self.assertEqual(r.status_code, 200)
    # POST request to /song to create a new song
    def test_2_add_new_song(self):
        r = requests.post(ApiTest.Create_URL, json=ApiTest.NewSongobj)
        self.assertEqual(r.status_code, 200)

    def test_2_add_new_podcast(self):
        r = requests.post(ApiTest.Create_URL, json=ApiTest.NewPodcastobj)
        self.assertEqual(r.status_code, 200)

    def test_2_add_new_Audiobook(self):
        r = requests.post(ApiTest.Create_URL, json=ApiTest.Newaudiobookobj)
        self.assertEqual(r.status_code, 200)

    def test_3_get_new_song(self):
        song_id = 4
        r = requests.get(self._get_each_song_url(song_id))
        self.assertEqual(r.status_code, 200)
        self.assertDictEqual(r.json(), ApiTest.Songobj)

    # PUT request to /song/song_id
    def test_4_update_existing_song(self):
        song_id = 3
        r = requests.post("{}/{}".format(ApiTest.update_URL,song_id),
                         json=ApiTest.updateSongobj)
        self.assertEqual(r.status_code, 200)

    # GET request to /song/song_id
    def test_5_get_new_song_after_update(self):
        song_id = 3
        r = requests.get(self._get_each_song_url(song_id))
        self.assertEqual(r.status_code, 200)
        self.assertDictEqual(r.json(), ApiTest.uSongobj)

    # DELETE request to /delete/song/song_id
    def test_6_delete_song(self):
        song_id = 6
        r = requests.get("{}/{}/{}".format(ApiTest.delete_url,"song",song_id))
        self.assertEqual(r.status_code, 200)

    def test_6_delete_audiobook(self):
        song_id = 2
        r = requests.get("{}/{}/{}".format(ApiTest.delete_url,"audiobook",song_id))
        self.assertEqual(r.status_code, 200)

    def test_6_delete_podcast(self):
        song_id = 3
        r = requests.get("{}/{}/{}".format(ApiTest.delete_url,"podcast",song_id))
        self.assertEqual(r.status_code, 200)

    @unittest.expectedFailure
    def test_7_get_new_song_after_delete(self):
        song_id = 6
        r = requests.get(self._get_each_song_url(song_id))
        self.assertEqual(r.status_code, 200)
