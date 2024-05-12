all : env run
	
git : per add commit push 
	
add : 
	git add .

commit :
	git commit -m "$(shell date +'%Y-%m-%d %H:%M')"

push :
	git push 

run :
	docker compose up -d 

down:
	docker compose down -v 

restart:down run

env:
	source env/bin/activate

per :
	sudo chmod -R 0777 .

clean : 
	docker compose  down 
	docker image prune -f --all