only if user is logged in in digikala.com
else, it should redirect user to https://www.digikala.com/users/login/?backUrl=/campaigns/oauth/authorize/

how to check if user logged in to digikala?
by sending a request including user credentials (specificly a cookie named `Digikala:User:Token:new`) to api.digikala.com/user/init/ we can see wether if user is authenticated in digikala or not
also, sometimes user has a login_token query parameter in the url, we should check for it too and pass it to the request
this endpoint always return a 200 http status, and in the json body of the response it has a is_logged_in key that is a boolean, if it is true it means the user is authenticated in digikala, it it is false it means the user is not authenticated in digikala

sample response (not logged in):
```json
{"status":200,"data":{"is_logged_in":false,"city":[],"show_location_modal":true,"modules":["67fa9476899309473e77fe4c832035d2","4c3e16c368b92c4fcd4db35d8d9fe93c","ed0a93864f5f3267b6e3c77c2b362d8f","dbc70bc2e88d7963d237b14f0f891f3a","27d2978e94438932ed89fc88f2e688bc","bd67dadd4f94e2e9e09237e9999feb13","f3aef7c016d40778dc21cd1ef0626bb3","8365e4c72e707e76603457792ab2a1b5","dfb5eabc9e44a7ed3f680338aed7660c","0cc0422bd5b6a5b109520224e9260a01","cade3be4f280116110067085e5bab6a2","3b25833fb72cf7334da9e015a87fbd22","dceb70f6e69fde39deaf5ff295e51243","8a8533666f9458dfc3f0cb2b6827298b","aafcbea2c8b0f1816899113c3854278d","2fa67d1e5e420380c17cfa08f1cb11a8","9cbd71591dda08518e4a7d47bbe8773e","f4304eaf0d1dc3d7a3f4ba8c4664912b","943478272d9437706babd1ec1cd33a00","6dd3bd7b037e5903df9e135bf7eb866b","dbaf7bdc7a05a20ee2a87ef1d365c58e","d57ba497c943027e70bb573d1c02a796","fef3d8299bb9287e17217e77b2d2717e","69c4728332a7a0f5aed0d70d2b4bd045","217469f5d25dc232f8909046046272e4","292e8cc6b3b89d1c8138cfd5bb8db096","10beb9d72b3fc36f40117b38284a0981","607a28a3b4bb4ceaa499e209e58ca9d7","8a067e4dbfecb492535abc7f04fc7433","1778ad80301bd78d3961a159d5f2c365","066219ba82ce65a4ae8e6903f9e51b05","da6b15b29b5c4ff1436052df402a2d3c","a41f113ef16659c6fa09ec236ac9138d","1507edb9a1ede0d56f2306c070d91270","b35ac6f190aac167cd72ff2eab3966ee","45aa09bc3651b0b9ab5e972aacb77a5b","55bff05106181403a6f0a4fc8a425e5c","1feba8b75c71f716a711eb7424bb1d53","1700d0f238046e76028560882aeea857","104422084ccbb9d51ffdff3b16c61ee6"],"date_time":"2025-01-20 19:45:43","social_profile":{"is_activated":false},"is_in_office":true,"promotion_top_banner":[]}}
```

sample response (logged in):
```json
{
"status": 200,
"data": {
"is_logged_in": true,
"digiclub": {
"is_digiclub_activated": true,
"points": 365,
"reward_url_threshold": 50,
"claimable_points": 0
},
"digiplus": {
"subscription_remaining_days": null,
"is_activated": false,
"user_state": "non_plus",
"is_general_location_jet_eligible": true
},
"notification": {
"notification": {
"count": 0
}
},
"user": {
"id": 3407819,
"first_name": "حسین",
"last_name": "تندرو",
"phone": "02155668499",
"city_id": 1698,
"mobile": "09124781329",
"email": "hossein9tondro@gmail.com",
"avatar_url": "https://api.digikala.com/static/files/fd4840b2.svg",
"is_legal": false,
"is_foreigner": false,
"has_password": true,
"personal_economic_number": null,
"verification_status": "verified",
"national_identity_number": "0019224362",
"gender": "female",
"birthday_iso": "1996-07-07",
"city_name": "تهران",
"state_name": "تهران",
"phone_hash": "80ded477d0dfa56d57c97662c52056a3"
},
"default_address": {
"id": 87165100,
"full_name": "حسین تندرو",
"address": "ونک، خیابان ولیعصر، خیابان خدامی، روبه روی هتل هما، جنب کوچه شادی ۱، پلاک ۳۱",
"postal_code": "1994753611",
"telephone": "",
"mobile": "989124781329",
"city_id": 1698,
"state_id": 9,
"district_id": 2858,
"support_fmcg": true,
"is_default": true,
"latitude": 35.76221,
"longitude": 51.40537,
"building_number": "31",
"unit": "10",
"drop_off_address_id": null,
"map_image": {
"storage_ids": {
"1": "f219297203096f21af93be93d85eaac3d8b9f7e3_1724201103"
},
"url": [
"https://dkstatics-public.digikala.com/digikala-static-map-images/f219297203096f21af93be93d85eaac3d8b9f7e3_1724201103.png"
],
"thumbnail_url": null,
"temporary_id": null,
"webp_url": [
"https://dkstatics-public.digikala.com/digikala-static-map-images/f219297203096f21af93be93d85eaac3d8b9f7e3_1724201103.png?x-oss-process=image/format,webp"
]
},
"is_usable": true,
"is_general_location_jet_eligible": true
},
"data_layer": {
"event": "user_attribute",
"data": {
"is_logged_in": true,
"user_id": 3407819,
"is_club_user": true,
"club_points": 365,
"rfm_category": "Loyal",
"total_delivered_orders": 66,
"aov": 24034155,
"magnet_membership": true,
"plus_membership": false,
"plus_membership_duration": 0
}
},
"show_location_modal": false,
"modules": [
"67fa9476899309473e77fe4c832035d2",
"4c3e16c368b92c4fcd4db35d8d9fe93c",
"ed0a93864f5f3267b6e3c77c2b362d8f",
"dbc70bc2e88d7963d237b14f0f891f3a",
"27d2978e94438932ed89fc88f2e688bc",
"bd67dadd4f94e2e9e09237e9999feb13",
"f3aef7c016d40778dc21cd1ef0626bb3",
"8365e4c72e707e76603457792ab2a1b5",
"dfb5eabc9e44a7ed3f680338aed7660c",
"0cc0422bd5b6a5b109520224e9260a01",
"cade3be4f280116110067085e5bab6a2",
"3b25833fb72cf7334da9e015a87fbd22",
"dceb70f6e69fde39deaf5ff295e51243",
"8a8533666f9458dfc3f0cb2b6827298b",
"aafcbea2c8b0f1816899113c3854278d",
"2fa67d1e5e420380c17cfa08f1cb11a8",
"9cbd71591dda08518e4a7d47bbe8773e",
"f4304eaf0d1dc3d7a3f4ba8c4664912b",
"943478272d9437706babd1ec1cd33a00",
"6dd3bd7b037e5903df9e135bf7eb866b",
"dbaf7bdc7a05a20ee2a87ef1d365c58e",
"d57ba497c943027e70bb573d1c02a796",
"fef3d8299bb9287e17217e77b2d2717e",
"69c4728332a7a0f5aed0d70d2b4bd045",
"217469f5d25dc232f8909046046272e4",
"292e8cc6b3b89d1c8138cfd5bb8db096",
"10beb9d72b3fc36f40117b38284a0981",
"607a28a3b4bb4ceaa499e209e58ca9d7",
"8a067e4dbfecb492535abc7f04fc7433",
"aacbb5777e611336c8bb8d6f8fc7ea80",
"ead6132a52fbc7dbb9ed747d2d8d4e1e",
"4f1855ff6677aa92c32ea953106a8cf4",
"e566f9bdd1e425c0f38fa52200d83bf7",
"e9e39c45bd0a40e5d11c30d2d2946380",
"1778ad80301bd78d3961a159d5f2c365",
"066219ba82ce65a4ae8e6903f9e51b05",
"da6b15b29b5c4ff1436052df402a2d3c",
"a41f113ef16659c6fa09ec236ac9138d",
"84546859439b2e9a62f20c4fd51e2d40",
"1507edb9a1ede0d56f2306c070d91270",
"b35ac6f190aac167cd72ff2eab3966ee",
"45aa09bc3651b0b9ab5e972aacb77a5b",
"55bff05106181403a6f0a4fc8a425e5c",
"ae864a90f3cbce200695a8a98e90a96c",
"1feba8b75c71f716a711eb7424bb1d53",
"1700d0f238046e76028560882aeea857",
"104422084ccbb9d51ffdff3b16c61ee6"
],
"date_time": "2025-01-20 19:45:39",
"social_profile": {
"is_activated": true,
"name": "حسین تندرو",
"username": "htondro",
"user_image": "https://dkstatics-public.digikala.com/digikala-content-x-profile/5b6dbc4320b529b31db0bf321fcf43e4b1dffb48_1726440298.jpg?x-oss-process=image/resize,m_lfit,h_300,w_300/quality,q_80"
},
"is_in_office": true,
"promotion_top_banner": []
}
}
```
