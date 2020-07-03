mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"shashank.vemuri1gmail.com.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\