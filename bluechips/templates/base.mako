<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <title>${self.title()}</title>
    ${h.stylesheet_link('%s/css/main.css' % request.script_name)}
    ${h.stylesheet_link('//ajax.googleapis.com/ajax/libs/jqueryui/1.7.2/themes/flick/jquery-ui.css')}
    ${h.javascript_link('//ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js')}
    ${h.javascript_link('//ajax.googleapis.com/ajax/libs/jqueryui/1.7.2/jquery-ui.min.js')}
    ${h.javascript_link('%s/js/admin.js' % request.script_name)}
  </head>
  <body>
    % if c.mobile_client:
      <div id="mobile">
        <a href="${h.url_for(request.url, use_non_mobile='no')}">Use mobile interface</a>
      </div>
    % endif
    <div id="nav" class="block">
      <table>
        <tr>
          <td>
            <h1 class="title">
              % if c.title:
                ${c.title}
              % else:
                BlueChips
              % endif
            </h1>
          </td>
          <td>
            <a href="${h.url_for(controller='status', action='index')}">
              <img src="${request.script_name}/icons/status.png" alt="">
              <span>Dashboard</span>
            </a>
          </td>
          <td>
            <a href="${h.url_for(controller='spend', action='index')}">
              <img src="${request.script_name}/icons/spend.png" alt="">
              <span>Expense</span>
            </a>
          </td>
          <td>
            <a href="${h.url_for(controller='transfer', action='index')}">
              <img src="${request.script_name}/icons/transfer.png" alt="">
              <span>Transfer</span>
            </a>
          </td>
          <td>
            <a href="${h.url_for(controller='history', action='index')}">
              <img src="${request.script_name}/icons/history.png" alt="">
              <span>History</span>
            </a>
          </td>
          <td>
            <a href="${h.url_for(controller='user', action='index')}">
              <img src="${request.script_name}/icons/user.png" alt="">
              <span>User</span>
            </a>
          </td>
        </tr>
      </table>
    </div>
    % for message in h.flash.pop_messages():
      <div class="flash">${str(message) | n}</div>
    % endfor
    <div id="content">
      ${next.body()}
    </div>
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

<%def name="listExpenditures(es)">
  <table class="list">
    <tr>
      <th class="date">Date</th>
      <th class="user">Spender</th>
      <th class="description">Description</th>
      <th class="amount">Amount</th>
      <th class="share">My Share</th>
      <th class="editlink"></th>
      <th class="deletelink"></th>
    </tr>
    % for e in es:
      <%
        if e.involves(request.environ['user']):
          klass = 'user-involved'
        else:
          klass = 'user-not-involved'
      %>
      <tr class="${klass}">
        <td class="date">${e.date}</td>
        <td class="user">${formatUser(e.spender)}</td>
        <td class="description">${e.description}</td>
        <td class="amount">${e.amount}</td>
        <td class="share">${e.share(request.environ['user'])}</td>
        <td class="editlink">${h.link_to('Edit', h.url_for(controller='spend', action='edit', id=e.id))}</td>
        <td class="deletelink">${h.link_to('Delete', h.url_for(controller='spend', action='delete', id=e.id))}</td>
      </tr>
    % endfor
  </table>
</%def>

<%def name="listTransfers(ts)">
  <table class="list">
    <tr>
      <th class="date">Date</th>
      <th class="user">From</th>
      <th class="user">To</th>
      <th class="description">Description</th>
      <th class="amount">Amount</th>
      <th class="editlink"></th>
      <th class="deletelink"></th>
    </tr>
    % for t in ts:
      <%
        if t.involves(request.environ['user']):
          klass = 'user-involved'
        else:
          klass = 'user-not-involved'
      %>
      <tr class="${klass}">
        <td class="date">${t.date}</td>
        <td class="user">${formatUser(t.debtor)}</td>
        <td class="user">${formatUser(t.creditor)}</td>
        <td class="description">${t.description}</td>
        <td class="amount">${t.amount}</td>
        <td class="editlink">${h.link_to('Edit', h.url_for(controller='transfer', action='edit', id=t.id))}</td>
        <td class="deletelink">${h.link_to('Delete', h.url_for(controller='transfer', action='delete', id=t.id))}</td>
      </tr>
    % endfor
  </table>
</%def>

<%def name="expenditureIcon()">
&larr;<span class="dollarsign">&rarr;
</%def>

<%def name="transferIcon()">
<span class="dollarsign">$</span>&rarr;<span class="dollarsign">$</span>
</%def>
