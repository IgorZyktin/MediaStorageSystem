# Browser configuration

# NGINX config
```
server {
    listen 80;
    root /home/pi/root;
    
    location /root/ {
        sendfile           on;
        sendfile_max_chunk 1m;
    }
    
    location / {
        proxy_pass http://localhost:5000/;
    }
}
```