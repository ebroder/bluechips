<%inherit file="/base.mako"/>

<p>Are you sure you want to delete this transfer?</p>

<form action="${h.url_for(controller='transfer', action='destroy', id=c.transfer.id)}" method="post">
  ${h.auth_token_hidden_field()}
  <table class="form">
    <tr>
      <th><label for="debtor_id">From</label></th>
      <td>${c.transfer.debtor}</td>
    </tr>
    <tr>
      <th><label for="creditor_id">To</label></th>
      <td>${c.transfer.creditor}</td>
    </tr>
    <tr>
      <th><label for="amount">Amount</label></th>
      <td>${c.transfer.amount}</td>
    </tr>
    <tr>
      <th><label for="date">Date</label></th>
      <td>${c.transfer.date.strftime('%m/%d/%Y')}</td>
    </tr>
    <tr>
      <th><label for="description">Description</label></th>
      <td>${c.transfer.description}</td>
    </tr>
    <tr>
      <td colspan="2">
        ${h.submit('delete', 'Delete', class_="submitbutton")}
        ${h.submit('cancel', 'Cancel', class_="submitbutton")}
      </td>
    </tr>
  </table>
</form>
