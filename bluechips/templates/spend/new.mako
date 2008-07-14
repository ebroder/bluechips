<%inherit file="/base.mako"/>

<%def name="title()">${parent.title()} :: Expenditure Details</%def>

<p>Expenditure logged.</p>

<h2>Want to do something unusual?</h2>

<ul id="expenditure_options">
  <li>${h.link_to('Change the split', h.url_for(action='split', id=c.expenditure.id))}</li>
  <li>${h.link_to('Spin off a subitem', h.url_for(action='subitem', id=c.expenditure.id))}</li>
</ul>
