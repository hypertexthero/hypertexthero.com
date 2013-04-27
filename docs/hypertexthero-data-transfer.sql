-- http://stackoverflow.com/questions/10968670/sqlite-data-from-one-db-to-another

hthdbimport.sqlite ->    hth.db                  
    import         ->        logbook_entries        
        LastMod    ->            pub_date        
        Title      ->            title           
        Body       ->            body            
        url_title  ->            slug            
        custom_1   ->            url             
                             taggit_tag      
        Keywords   ->            name        


-- commands (Thanks, Paola!)

sqlite3 hth.db

attach database 'hthdbimport.sqlite' as txpdb;

insert into logbook_entries (pub_date,mod_date,title,body,body_html,content_format,is_active,slug,url,kind) select Posted,LastMod,Title,Body,Body_html,'markdown','1',url_title,custom_1,'L' from txpdb.hypertexthero_db;
    
    
    
CREATE TABLE "logbook_entries" (
    "id" integer NOT NULL PRIMARY KEY,
    "title" varchar(200) NOT NULL,
    "slug" varchar(50) NOT NULL,
    "kind" varchar(1) NOT NULL,
    "url" varchar(200) NULL,
    "body" text NULL,
    "body_html" text NULL,
    "content_format" varchar(50) NOT NULL,
    "is_active" bool NOT NULL,
    "pub_date" datetime NOT NULL,
    "mod_date" datetime NOT NULL
)