<%inherit file="/base.mako"/>

<h2>Email Notifications</h2>

<p>Enter an email address below if you wish to be notified of any updates to transactions involving you. Leave blank to not receive notifications.</p>
<form action="${h.url_for(controller='user', action='update')}" method="post">
  ${h.auth_token_hidden_field()}
  <table class="form">
    <tr>
      <th><label for="new_email">Email</label></th>
      <td>${h.text('new_email', request.environ['user'].email, size=48)}</td>
      <td><input type="submit" value="Update" /></td>
    </tr>
  </table>
</form>
