from postmarker.core import PostmarkClient
postmark = PostmarkClient(server_token='5e1c1fd1-2f04-412c-a593-f8259026b1a9')
postmark.emails.send(
  From='vsingh287@west-mec.org',
  To='vsingh287@west-mec.org',
  Subject='Postmark test',
  HtmlBody='HTML body goes here'
)