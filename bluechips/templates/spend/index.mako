<%inherit file="/base.mako"/>

<%!
    from decimal import Decimal
%>

<form action="${h.url_for(controller='spend', action='update', id=c.expenditure.id)}" method="post">
  ${h.auth_token_hidden_field()}
  <table class="form">
    <tr>
      <th><label for="spender_id">Spender</label></th>
      <td>${h.select('spender_id', c.expenditure.spender_id, c.users)}</td>
    </tr>
    <tr>
      <th><label for="amount">Amount</label></th>
      <td>${h.currency('amount', c.expenditure.amount, size=8)}</td>
    </tr>
    <tr>
      <th><label for="date">Date</label></th>
      <td>${h.text('date', c.expenditure.date.strftime('%m/%d/%Y'), size=16, class_='datepicker')}</td>
    </tr>
    <tr>
      <th><label for="description">Description</label></th>
      <td>${h.text('description', c.expenditure.description, size=64)}</td>
    </tr>
  </table>

  <p>Change how an expenditure is split up. Enter a percentage, or something like a percentage, for each user. They don't have to add to 100.</p>

  <table class="form">
    % for ii, user_row in enumerate(c.users):
      <%
        user_id, user = user_row
        percent = c.values['shares-%d.amount' % ii]
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
