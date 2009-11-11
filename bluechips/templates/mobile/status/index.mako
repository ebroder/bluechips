<%inherit file="/mobile/base.mako"/>

<%!
  from datetime import date
%>

<div id="tabs">
  <a id="status" class="selected" href="#">
    <img src="/icons/dashboard.png" alt="">
    <span>Dashboard</span>
  </a>
  <a id="spend" href="#">
    <img src="/icons/spend.png" alt="">
    <span>Expense</span>
  </a>
  <a id="transfer" href="#">
    <img src="/icons/transfer.png" alt="">
    <span>Transfer</span>
  </a>
</div>

<div id="tab-status" class="tab">
  % for message in h.flash.pop_messages():
    <div class="flash">${message | n}</div>
  % endfor

  % if len(c.settle) == 0:
    <p>No need! The books are balanced!</p>
  % else:
    <p>To balance the books, the following transfers need to be made:</p>

    <table id="balance">
      <tr>
        <th>From</th>
        <th>To</th>
        <th>Amount</th>
      </tr>
      % for transfer in c.settle:
        <tr>
          <td>${transfer[0].name}</td>
          <td>${transfer[1].name}</td>
          <td>${transfer[2]}</td>
        </tr>
      % endfor
    </table>
  % endif
</div>

<div id="tab-spend" class="tab">
  <form action="${h.url_for(controller='spend', action='update')}" method="post">
    ${h.auth_token_hidden_field()}
    <table class="form">
      <tr>
        <th><label for="spender_id">Spender</label></th>
        <td>${h.select('spender_id', [request.environ['user'].id], c.users)}</td>
      </tr>
      <tr>
        <th><label for="amount">Amount</label></th>
        <td>${h.currency('amount', 0, size=8)}</td>
      </tr>
      <tr>
        <th><label for="date">Date</label></th>
        <td>${h.text('date', date.today().strftime('%m/%d/%Y'), size=16)}</td>
      </tr>
      <tr>
        <th><label for="description">Description</label></th>
        <td>${h.text('description')}</td>
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

<div id="tab-transfer" class="tab">
  <form action="${h.url_for(controller='transfer', action='update')}" method="post">
    ${h.auth_token_hidden_field()}
    <table class="form">
      <tr>
        <th><label for="debtor_id">From</label></th>
        <td>${h.select('debtor_id', request.environ['user'].id, c.users)}</td>
      </tr>
      <tr>
        <th><label for="creditor_id">To</label></th>
        <td>${h.select('creditor_id', None, c.users)}</td>
      </tr>
      <tr>
        <th><label for="amount">Amount</label></th>
        <td>${h.currency('amount', 0, size=8)}</td>
      </tr>
      <tr>
        <th><label for="date">Date</label></th>
        <td>${h.text('date', date.today().strftime('%m/%d/%Y'), size=16)}</td>
      </tr>
      <tr>
        <th><label for="description">Description</label></th>
        <td>${h.text('description')}</td>
      </tr>
      <tr>
        <td colspan="2">
          <input type="submit" value="Submit" />
        </td>
      </tr>
    </table>
  </form>
</div>
