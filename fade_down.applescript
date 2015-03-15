on is_playing(name)
	local state
	set state to false
	if application name is running then
		if name is "iTunes" then
			tell application "iTunes" to set state to player state is playing
		else if name is "Rdio" then
			tell application "Rdio" to set state to player state is playing
		else if name is "VLC" then
			tell application "VLC" to set state to playing
		end if
	end if
	return state
end is_playing

on current_volume(name)
	local v
	if name is "iTunes" then
		tell application "iTunes" to set v to sound volume
	else if name is "Rdio" then
		tell application "Rdio" to set v to sound volume
	else if name is "VLC" then
		tell application "VLC" to set v to audio volume
	end if
	return v
end current_volume

on fade(name, delay_, start_volume, end_volume)
	-- set the step size based on whether start or end volume is bigger
	set step_ to (((start_volume < end_volume) as integer) * 2 - 1)
	
	repeat with i from start_volume to end_volume by step_
		if name is "iTunes" then
			tell application "iTunes" to set the sound volume to i
		else if name is "Rdio" then
			tell application "Rdio" to set the sound volume to i
		else if name is "VLC" then
			tell application "VLC" to set the audio volume to i
		end if
		delay delay_
	end repeat
end fade

on fade_down(name)
	if is_playing(name) then
		set v to current_volume(name)
		fade(name, 0.01, v, v / 3)
	end if
end fade_down

on fade_up(name)
	if is_playing(name) then
		set v to current_volume(name)
		fade(name, 0.01, v, v * 3)
	end if
end fade_up

on fade_down_all()
	fade_down("VLC")
	fade_down("Rdio")
	fade_down("iTunes")
end fade_down_all

on fade_up_all()
	fade_up("VLC")
	fade_up("Rdio")
	fade_up("iTunes")
end fade_up_all

fade_down_all()