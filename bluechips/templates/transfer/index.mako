<%inherit file="/base.mako"/>

<form action="${h.url_for(controller='transfer', action='update', id=c.transfer.id)}" method="post">
  ${h.auth_token_hidden_field()}
  <table class="form">
    <tr>
      <th><label for="debtor_id">From</label></th>
      <td>${h.select('debtor_id', c.transfer.debtor_id, c.users)}</td>
    </tr>
    <tr>
      <th><label for="creditor_id">To</label></th>
      <td>${h.select('creditor_id', c.transfer.creditor_id, c.users)}</td>
    </tr>
    <tr>
      <th><label for="amount">Amount</label></th>
      <td>${h.currency('amount', c.transfer.amount, size=8)}</td>
    </tr>
    <tr>
      <th><label for="date">Date</label></th>
      <%
        if c.transfer.date is None:
            date_string = ''
        else:
            date_string = c.transfer.date.strftime('%m/%d/%Y')
      %>
      <td>${h.text('date', date_string, size=16, class_='datepicker')}</td>
    </tr>
    <tr>
      <th><label for="description">Description</label></th>
      <td>${h.text('description', c.transfer.description, size=64)}</td>
    </tr>
    <tr>
      <td colspan="2">
        <input type="submit" value="Submit" />
      </td>
    </tr>
  </table>
</form>
