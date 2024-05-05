import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

import Alert, { DefaultAlert } from '../components/Alert';
import LinkEditForm from '../components/forms/LinkEdit';
import NotFound from './NotFound';
import Preloader from '../components/Preloader';
import getLink from '../js/api/getLink';
import logOutRequest from '../js/api/logOut';

export default function Link() {
  const id = useParams().id;
  const [link, setLink] = useState({});
  const [alert, setAlert] = useState(DefaultAlert);
  const [noContent, setNoContent] = useState(false);

  // Effect to load link data
  useEffect(() => {
    getLink(id).then((data) => {
      const error_code = data.detail;
      if (error_code !== undefined) {
        error_code === 18 ? setNoContent(true) : logOutRequest();
      } else {
        const { title, tags, url, annotation } = data;
        setLink({
          title: title,
          tags: tags ? tags : [],
          url: url,
          annotation: annotation,
        });
      }
    });
  }, [id]);

  return (
    <>
      {noContent ? (
        <NotFound />
      ) : !Object.keys(link).length ? (
        <Preloader />
      ) : (
        <div className='container'>
          {alert.isVisible ? <Alert alert={alert} setAlert={setAlert} /> : null}
          <LinkEditForm
            id={id}
            link={link}
            setLink={setLink}
            setAlert={setAlert}
          />
        </div>
      )}
    </>
  );
}
