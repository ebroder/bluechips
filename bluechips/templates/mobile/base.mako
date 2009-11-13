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
    % for message in h.flash.pop_messages():
      <div class="flash">${message | n}</div>
    % endfor
    ${next.body()}
    <div id="non-mobile">
      <a href="${h.url_for(request.url, use_non_mobile='yes')}">Use non mobile interface</a>
    </div>
    ${h.javascript_link('/js/jquery-1.3.2.js')}
    ${h.javascript_link('/js/mobile.js')}
  </body>
</html>

<%!
  from datetime import date
%>

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

<%def name="tabs(selected)">
  <div id="tabs">
    % for name in ('status', 'spend', 'transfer'):
      <%
        if name == selected:
          klass = 'selected'
        else:
          klass = 'unselected'
      %>
      <a id="${name}" class="${klass}" href="${h.url_for(controller=name, action='index', id=None)}">
        <img src="/icons/${name}.png" alt="">
        <span>${name.capitalize()}</span>
      </a>
    % endfor
  </div>
</%def>

<%def name="spendForm()">
  <div id="tab-spend" class="tab">
    <%
      if c.id != '':
          id = c.id
      else:
          id = None
    %>
    <form action="${h.url_for(controller='spend', action='update', id=id)}" method="post">
      ${h.auth_token_hidden_field()}
      <table class="form">
        <tr>
          <th><label for="spender_id">Spender</label></th>
          <td>${h.select('spender_id', [h.grab(c.expenditure, 'spender_id')], c.users)}</td>
        </tr>
        <tr>
          <th><label for="amount">Amount</label></th>
          <td>${h.currency('amount', h.grab(c.expenditure, 'amount'), size=8)}</td>
        </tr>
        <tr>
          <th><label for="date">Date</label></th>
          <td>${h.text('date', h.grab(c.expenditure, 'date').strftime('%m/%d/%Y'), size=16)}</td>
        </tr>
        <tr>
          <th><label for="description">Description</label></th>
          <td>${h.text('description', h.grab(c.expenditure, 'description'))}</td>
        </tr>
      </table>

      <p>Change how an expenditure is split up.</p>

      <table class="form">
        % for ii, user_row in enumerate(c.users):
          <%
            user_id, user = user_row
            if user.resident:
              percent = 1
            else:
              percent = 0
          %>
          <tr>
            <th><label for="shares-${ii}amount">${user.name}</label></th>
            <td>
              ${h.text('shares-%d.amount' % ii, percent)}
              ${h.hidden('shares-%d.user_id' % ii, user.id)}
            </td>
          </tr>
        % endfor
        <tr>
          <td colspan="2">
            ${h.submit(None, 'Submit', class_="submitbutton")}
          </td>
        </tr>
      </table>
    </form>
  </div>
</%def>

<%def name="transferForm()">
  <%
    if c.id != '':
        id = c.id
    else:
        id = None
  %>
  <div id="tab-transfer" class="tab">
    <form action="${h.url_for(controller='transfer', action='update', id=id)}" method="post">
      ${h.auth_token_hidden_field()}
      <table class="form">
        <tr>
          <th><label for="debtor_id">From</label></th>
          <td>${h.select('debtor_id', [h.grab(c.transfer, 'debtor_id')], c.users)}</td>
        </tr>
        <tr>
          <th><label for="creditor_id">To</label></th>
          <td>${h.select('creditor_id', [h.grab(c.transfer, 'creditor_id')], c.users)}</td>
        </tr>
        <tr>
          <th><label for="amount">Amount</label></th>
          <td>${h.currency('amount', h.grab(c.transfer, 'amount'), size=8)}</td>
        </tr>
        <tr>
          <th><label for="date">Date</label></th>
          <td>${h.text('date', h.grab(c.transfer, 'date').strftime('%m/%d/%Y'), size=16)}</td>
        </tr>
        <tr>
          <th><label for="description">Description</label></th>
          <td>${h.text('description', h.grab(c.transfer, 'description'))}</td>
        </tr>
        <tr>
          <td colspan="2">
            <input type="submit" value="Submit" />
          </td>
        </tr>
      </table>
    </form>
  </div>
</%def>
