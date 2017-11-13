from interface_drive import shareVideo as driveShare

def uploadAll(title, message, path):
	print driveShare(title, path, ['arnaubennassar5@gmail.com', 'arnaubf@openmailbox.org'])

uploadAll('test', 'Fent unes proves de tranquis', '/Users/arnaubennassarformenti/Downloads/Volley_Feroe_cut_min38.30.mp4')