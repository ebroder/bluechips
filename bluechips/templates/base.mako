<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <title>${self.title()}</title>
    ${h.stylesheet_link('/css/main.css')}
  </head>
  <body>
    <% messages = h.flash.pop_messages() %>
    % if messages:
    <ul id="flash-messages">
    % for message in messages:
        <li>${message}</li>
    % endfor
    </ul>
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
            <a href="${h.url_for(controller='status', action='index', id=None)}">
              <img src="/icons/dashboard.png" alt="">
              <span>Dashboard</span>
            </a>
          </td>
          <td>
            <a href="${h.url_for(controller='spend', action='index', id=None)}">
              <img src="/icons/spend.png" alt="">
              <span>Expense</span>
            </a>
          </td>
          <td>
            <a href="${h.url_for(controller='transfer', action='index', id=None)}">
              <img src="/icons/transfer.png" alt="">
              <span>Transfer</span>
            </a>
          </td>
          <td>
            <a href="${h.url_for(controller='history', action='index', id=None)}">
              <img src="/icons/history.png" alt="">
              <span>History</span>
            </a>
          </td>
        </tr>
      </table>
    </div>
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
  % if user == c.user:
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
      <th class="editlink"></th>
    </tr>
    % for e in es:
      <%
        if e.involves(c.user):
          klass = 'user-involved'
        else:
          klass = 'user-not-involved'
      %>
      <tr class="${klass}">
        <td class="date">${e.date}</td>
        <td class="user">${formatUser(e.spender)}</td>
        <td class="description">${e.description}</td>
        <td class="amount">${e.amount}</td>
        <td class="editlink">${h.link_to('Edit', h.url_for(controller='spend', action='edit', id=e.id))}</td>
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
    </tr>
    % for t in ts:
      <%
        if t.involves(c.user):
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
