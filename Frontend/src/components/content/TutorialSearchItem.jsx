import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import $ from 'jquery';

import '../../css/components/search.css';

import Tag from '../tags/Tag';

export default function TutorialSearchItem(props) {
  const { id, title, tags, isDeleteMode, postsToDelete, setPostsToDelete } =
    props;
  const navigate = useNavigate();

  const setDeleteStyle = () => {
    $('#checkbox-' + id).prop('checked', true);
    $('#card-' + id).css({ backgroundColor: 'var(--color1)' });
  };

  const removeDeleteStyle = () => {
    $('#checkbox-' + id).prop('checked', false);
    $('#card-' + id).css({ backgroundColor: 'white' });
  };

  const handleClick = (event) => {
    if (!event.target.classList.contains('card-link')) {
      if (isDeleteMode) {
        if (postsToDelete.includes(id)) {
          setPostsToDelete((oldPosts) =>
            [...oldPosts].filter((postId) => postId !== id)
          );
          removeDeleteStyle();
        } else {
          setPostsToDelete((oldPosts) => [...oldPosts, id]);
          setDeleteStyle();
        }
      } else {
        navigate(`/manage_content/tutorials/${id}`);
      }
    }
  };

  // Effect to remove delete style when switching off delete mode
  useEffect(() => {
    if (!isDeleteMode) removeDeleteStyle();
    // eslint-disable-next-line
  }, [isDeleteMode]);

  return (
    <div className='card mb-2' onClick={handleClick}>
      <div id={'card-' + id} className='card-body'>
        <div className='d-flex flex-row align-items-start justify-content-between'>
          <h5 className='d-block card-title'>{title}</h5>
          {isDeleteMode ? (
            <input
              className='form-check-input ms-2'
              type='checkbox'
              value=''
              id={'checkbox-' + id}
              style={{ cursor: 'pointer' }}
            />
          ) : null}
        </div>
        <h6 className='card-subtitle mb-2 text-body-secondary'>
          <div
            className='d-flex flex-wrap'
            style={{ width: '100% !important' }}
          >
            {tags.map((tag, index) => (
              <Tag key={index} name={tag} removeOption={false} />
            ))}
          </div>
        </h6>
        <div className='d-flex justify-content-end'>
          <div
            className='content-type-identifier'
            style={{ backgroundColor: '#cc99ff' }}
          >
            tutorial
          </div>
        </div>
      </div>
    </div>
  );
}
