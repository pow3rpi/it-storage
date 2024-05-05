import { useState } from 'react';

import Alert, { DefaultAlert } from '../components/Alert';
import LinkCreateForm from '../components/forms/LinkCreate';

export default function LinkCreate() {
  const defaultValue = { title: '', tags: [], url: '', annotation: '' };
  const [alert, setAlert] = useState(DefaultAlert);

  return (
    <div className='container'>
      {alert.isVisible ? <Alert alert={alert} setAlert={setAlert} /> : null}
      <div className='row'>
        <div className='col-12'>
          <h2 className='text-center mb-5 mt-lg-5'>Create Link</h2>
        </div>
      </div>
      <LinkCreateForm defaultValue={defaultValue} setAlert={setAlert} />
    </div>
  );
}
