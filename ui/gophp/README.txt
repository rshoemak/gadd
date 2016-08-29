August 26, 2016

file "device_data_template.txt" in this current directory "gophp"
is a duplicate of the file directory "gadd".

I consider 'gadd/device_data_template.txt' to be the source of truth.
All changes should be made on gadd/device_data_template.txt' and replicated on "gophp/device_data_template.txt" unless
you have very specific reason not to.

I did this because php is looking for the 'device_data_template.txt' in the root of the php server when the main page
is started 'index2.php'

I know this isn't optimal, I need to redo the directory structure at a later date.

