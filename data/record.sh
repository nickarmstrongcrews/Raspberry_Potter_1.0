# first open cheese app in linux start menu
# run next command and then click on the cheese window
window_id=$(xwininfo | awk '/Window id:/ {print $4}')
sleep 5 && recordmydesktop --windowid $window_id
