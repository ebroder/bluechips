<%inherit file="/base.mako"/>

<p>Are you sure you want to delete this expenditure?</p>

<form action="${h.url_for(controller='spend', action='destroy', id=c.expenditure.id)}" method="post">
  ${h.auth_token_hidden_field()}
  <table class="form">
    <tr>
      <th><label for="spender_id">Spender</label></th>
      <td>${c.expenditure.spender.name}</td>
    </tr>
    <tr>
      <th><label for="amount">Amount</label></th>
      <td>${c.expenditure.amount}</td>
    </tr>
    <tr>
      <th><label for="date">Date</label></th>
      <td>${c.expenditure.date.strftime('%m/%d/%Y')}</td>
    </tr>
    <tr>
      <th><label for="description">Description</label></th>
      <td>${c.expenditure.description}</td>
    </tr>
    <tr>
      <td colspan="2">
        ${h.submit('delete', 'Delete', class_="submitbutton")}
        ${h.submit('cancel', 'Cancel', class_="submitbutton")}
      </td>
    </tr>
  </table>
</form>
