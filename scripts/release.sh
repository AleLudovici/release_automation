#! /bin/sh

set -e

credentials_file="credentials.txt"
token=$(cat "$credentials_file")
release_json_file="$1"

function is_branch_clean() {
	if output=$(git status --porcelain) && [ -z "$output" ]; then
		true
	else 
	  	echo 'You have uncommitted changes. Please commit them before releasing.'
	  	false
	fi
}

function is_json_provided() {
	if [ -n "$release_json_file" ] && [[ $release_json_file =~ ([a-zA-Z0-9\s_\\.\-\(\):])+(.json)$ ]]; then
	  	true
	else
		echo 'Please provide a json file to draft the release.'
		false
	fi
}

function is_json_valid() {
	if validation=$(python -mjson.tool "$release_json_file" > /dev/null) && [ -z "$validation" ]; then 
	  	true
	 else
	  	false
	 fi
}

function check_prerequisites() {
	is_json_provided && is_json_valid
}

function merge_master_to_release() {
	git checkout master &&
	git pull &&
	git checkout release &&
	git merge master
}

function build() {
	echo 'Building project...'
	xcodebuild clean build \
	-project release\ automation.xcodeproj \
	-UseModernBuildSystem=NO \
	-sdk iphonesimulator \
	-destination "name=iPhone 8"
}

function push() {
	git push origin release
}

function draft_release() {
	echo 'Creating release draft'
	curl -H "Authorization: token $token" -d "@$release_json_file" https://api.github.com/repos/AleLudovici/release_automation/releases
}

if check_prerequisites; then
	merge_master_to_release
  	build
  	push
  	draft_release
fi
