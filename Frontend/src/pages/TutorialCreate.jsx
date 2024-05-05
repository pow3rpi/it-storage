import { useState } from 'react';

import Alert, { DefaultAlert } from '../components/Alert';
import TutorialCreateForm from '../components/forms/TutorialCreate';

export default function TutorialCreate() {
  const defaultValue = { title: '', tags: [], file: '', size: 0 };
  const [alert, setAlert] = useState(DefaultAlert);

  return (
    <div className='container'>
      {alert.isVisible ? <Alert alert={alert} setAlert={setAlert} /> : null}
      <div className='row'>
        <div className='col-12'>
          <h2 className='text-center mb-5 mt-lg-5'>Create Tutorial</h2>
        </div>
      </div>
      <TutorialCreateForm defaultValue={defaultValue} setAlert={setAlert} />
    </div>
  );
}
