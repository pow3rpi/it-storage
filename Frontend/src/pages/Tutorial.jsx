import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

import Alert, { DefaultAlert } from '../components/Alert';
import NotFound from './NotFound';
import Preloader from '../components/Preloader';
import TutorialEditForm from '../components/forms/TutorialEdit';
import getTutorial from '../js/api/getTutorial';
import logOutRequest from '../js/api/logOut';

export default function Tutorial() {
  const id = useParams().id;
  const [tutorial, setTutorial] = useState({});
  const [alert, setAlert] = useState(DefaultAlert);
  const [noContent, setNoContent] = useState(false);

  // Effect to load tutorial data
  useEffect(() => {
    getTutorial(id).then((data) => {
      const error_code = data.detail;
      if (error_code !== undefined) {
        error_code === 18 ? setNoContent(true) : logOutRequest();
      } else {
        const { title, tags, file } = data;
        setTutorial({
          title: title,
          tags: tags ? tags : [],
          file: file,
          size: new Blob([file]).size,
        });
      }
    });
  }, [id]);

  return (
    <>
      {noContent ? (
        <NotFound />
      ) : !Object.keys(tutorial).length ? (
        <Preloader />
      ) : (
        <div className='container'>
          {alert.isVisible ? <Alert alert={alert} setAlert={setAlert} /> : null}
          <TutorialEditForm
            id={id}
            tutorial={tutorial}
            setTutorial={setTutorial}
            setAlert={setAlert}
          />
        </div>
      )}
    </>
  );
}
