<%inherit file="/base.mako"/>

<h2>User Settings</h2>

<ul>
  <li><a href="${h.url_for(controller='user', action='email')}">Set e-mail address</a></li>
% if request.environ['user'].resident:
  <li><a href="${h.url_for(controller='user', action='new')}">Register a new user</a></li>
% endif
</ul>
