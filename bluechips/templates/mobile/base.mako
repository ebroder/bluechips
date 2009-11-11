<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <title>${self.title()}</title>
    ${h.stylesheet_link('/css/main.css')}
    <link media="only screen and (max-device-width: 480px)" href="/css/mobile.css" type="text/css" rel="stylesheet">
    <meta name="viewport" content="width = device-width, user-scalable=no">
    <link rel="apple-touch-icon" href="/icons/apple-touch.png">
  </head>
  <body>
    ${next.body()}
    ${h.javascript_link('/js/jquery-1.3.2.js')}
    ${h.javascript_link('/js/mobile.js')}
  </body>
</html>

<%def name="title()">BlueChips
% if c.title != '':
  :: ${c.title}
% endif
</%def>

<%def name="formatUser(user)">
  % if user == request.environ['user']:
    <strong>Me</strong>
  % else:
    ${user.name}
  % endif
</%def>
