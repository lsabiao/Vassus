echo "Are you root?!\033[1;40;34m ಠ_ಠ \033[m"
ROOTUID="0"
if [ "$(id -u)" -ne "$ROOTUID" ] ; then
    echo "\033[0;30;41mYou must be root to run this script\033[1;40;31m u.u\033[m"
    exit 1
fi
echo "Yes \033[1;40;34m( ͡° ͜ʖ ͡°)\033[m"
#end the root check

#install pillow (PIL)
#echo "installing pillow using pip"
#sudo pip install pillow

echo "cping vassus.py to /usr/bin as vassus"
cp vassus.py /usr/bin/vassus
echo "setting permissions"
chmod +x /usr/bin/vassus


echo "DONE"
