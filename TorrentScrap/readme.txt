1. It will search for valid domain based from domain.txt
2. From google search result , it will check each and very URL 
3. One valid torrent site found, it will look for malayalam folder
4. it will save the films on movie.txt
5. Comment # starts of the line will make script to look for movie name again from torrent site
6. Delete the movie Name from movie.txt , script will look for movie Link again from torrent site

Edit : config.json  for proxy server and google Search key


Example of output :

./torrentSeacrch.py 
From history domain name is lv
Trying with http://tamilrockers.lv
Blocked
Will search in google 
https://play.google.com/store/apps/details?id=tamilrockers.movies&hl=en
http://9to5google.com/2016/12/01/how-to-download-movies-and-shows-in-the-netflix-app-for-android/
http://tamilrockers.nz/
https://www.youtube.com/watch?v=pYWKcRlFnOM
http://playtamil.in/Tamilrockers-movies/
[u'http://tamilrockers.nz']
Trying with http://tamilrockers.nz
GoodURL URL
working domain http://tamilrockers.nz
will do things with http://tamilrockers.nz/index.php/forum/124-malayalam-movies/
^^^^^^^^^^^^^^^^^^^^^^^^^^^
New Movie found Avarude Raavukal (2017) 
Download Link
http://tamilrockers.nz/index.php/topic/59461-avarude-raavukal-2017-malayalam-dvdrip-xvid-mp3-700mb-esubs/       
***************************
New Movies ['Avarude Raavukal (2017) ']
