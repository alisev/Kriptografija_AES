Programma ziņojumu iekodēšanai un atkodēšanai, izmantojot AES algoritmu ar CBC vai CFB režīmu.

Programma ir uzrakstīta valodā Python 3.6 un izmanto vairākas bibliotēkas tās darbības nodrošināšanai:
	- Crypto	Pycryptodome bibliotēka. Nodrošina iekodēšanu un atkodēšanu ar AES.
	- argparse	Ļauj ievadīt programmā parametrus no komandrindiņas.
	- os		Tiek izmantots, lai iegūtu uzģenerētu IV priekš CFB režīma.
	- datetime	Ļauj izveidot laika zīmogu. Tiek izmantots izvaddatņu nosaukšanai.
	- typing	Ļauj norādīt datu tipus funkcijām. Pirmkoda lasāmības uzlabošanai.

----
Darbs ar programmu:

0) Programmas palaišanai ir nepieciešams, lai uz datora būtu uzinstalēts Python 3.10. Iespējams, ka derēs arī citas Python 3 versijas, bet par to negalvoju. Gadījumā, ja programma izmet "ModuleNotFoundError" kļūdas paziņojumu, tad trūkstošo moduli var uzinstalēt ar 'pip install <module>' komandu.

1) Programmu palaiž caur komandrindiņu vienlaikus secīgi norādot:
	-f vai --filename:		Ceļš uz datni, kas satur ziņojumu un atslēgu.
	-cmode vai --chainingmode:	Savirknēšanas režīms. Pieļaujamās vērtības ir "CBC" un "CFB".
	-d vai --direction:		Kodēšanas virziens. Pieļaujamās vērtības ir "E" iekodēšanai un "D" dekodēšanai.
	-mac:				MAC vērtība, ja tiek izmantots CFB režīms. Citādi var atstāt tukšu.

Komandu piemēri:
	python Kriptografija.py -f ./input/input_01.txt -cmode CBC -d E
	python Kriptografija.py -f ./input/input_05.txt -cmode CFB -d D -mac ./input/input_05_MAC.txt

2) Pēc uzdevuma izpildīšanas programma uz ekrāna parādīs rezultātu un saglabās informāciju binārā datnē, kas ir atrodams programmas mapē 'MD1/output'.
Ja tika izmantota iekodēšana ar CFB savirknēšanas režīmu, tad izvadfailā tiek saglabāta ne tikai iekodētā virkne, bet arī uzģenerētā IV vērtība (kas ir atdalītas ar 8 "\x00") un kā arī .bin fails ar MAC vērtību. MAC vērtības faila nosaukums ir iegūts, atbilstošajam rezultāta faila nosaukumam pievienojot beigās '_MAC'. Piemēram:
	- output20220424-121345.bin
	- output20220424-121345_MAC.bin

----
Iekļautie piemēri mapē input:

	input_01.txt	Piemērs iekodēšanai, kur nav nepieciešams padding.
	input_02.txt	Piemērs iekodēšanai, kur padding var būt nepieciešams.

	input_03.txt	Piemērs dekodēšanai, kas iegūts, iekodējot input_01.txt ar AES un CBC.
	input_04.txt	Piemērs dekodēšanai, kas iegūts, iekodējot input_02.txt ar AES un CBC.
	
	input_05.txt	Piemērs dekodēšanai, kas iegūts, iekodējot input_01.txt ar AES un CFB.
	input_05_MAC.txt
	input_06.txt	Piemērs dekodēšanai, kas iegūts, iekodējot input_02.txt ar AES un CFB.
	input_06_MAC.txt
	
----
Par generate_key.py:

Tā ir programma atslēgu ģenerēšanai. To palaiž caur komandrindiņu un lietotājs var norādīt neobligātus argumentus:
	-l vai -length - Atslēgas garums baitos. Pieļaujamās vērtības: 16, 24, 32. Noklusējuma vērtība ir 16.
	-p vai -passphrase - Simbolu virkne, kas tiek pielietota atslēgas ģenerēšanā. Ja nav norādīta, tad noklusējuma vērtība ir tukša simbolu virkne un programma uzģenerē atslēgu ar os.urandom() funkciju.

Daži derīgi komandu piemēri:
	python generate_key.py
	python generate_key.py -l 32
	python generate_key.py -p "Hello, World!"
	python generate_key.py -l 32 -p "Hello, World!"

Uzģenerētā atslēga tiek saglabāta .txt failā mapē output un to nosaukumi sākas ar "KEY_". Vērtības tiek uzglabātas heksadecimālā formāta un tās var iekopēt ievades failā tālākai izmantošanai.
