<%inherit file="/base.mako"/>

<h2>Register a New User</h2>

<form action="${h.url_for(controller='user', action='create')}" method="post">
  ${h.auth_token_hidden_field()}
  <table class="form">
    <tr>
      <th><label for="username">Username</label></th>
      <td>${h.text('username', size=32)}</td>
    </tr>
## If you used a password to authenticate, we'll ask for
## one. Otherwise, we assume you didn't use our authn stack to
## authenticate
% if request.environ.get('AUTH_TYPE') == 'basic':
    <tr>
      <th><label for="password">Password</label></th>
      <td>${h.password('password', size=32)}</td>
    </tr>
    <tr>
      <th><label for="confirm_password">Confirm password</label></th>
      <td>${h.password('confirm_password', size=32)}</td>
    </tr>
% endif
    <tr>
      <th><label for="name">Display name</label></th>
      <td>${h.text('name', size=32)}</td>
    </tr>
    <tr>
      <th>Resident</th>
      <td><label>${h.radio('resident', '1')} Yes</label>
        <label>${h.radio('resident', '0', checked='checked')} No</label></td>
    </tr>
  </table>
  <p>Residents are included by default in new expenditures.</p>
  <table class="form">
    <tr>
      <td colspan="2">
        <input class="submitbutton" id="none" type="submit" value="Submit" />
      </td>
    </tr>
  </table>
</form>
