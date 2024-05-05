import Tag from '../components/tags/Tag';

import '../css/layout/linkPreview.css';

export default function LinkPreview(props) {
  const { title, tags, url, annotation } = props;

  return (
    <>
      <div className='link-preview-title'>Title</div>
      <div className='link-preview-value mb-3'>{title}</div>
      <div className='link-preview-title'>Topics</div>
      <div className='link-preview-value mb-3 col-12 d-flex flex-wrap'>
        {!tags.length ? (
          <div>No topics</div>
        ) : (
          tags.map((tag, index) => (
            <Tag key={index} name={tag} removeOption={false} />
          ))
        )}
      </div>
      <div className='link-preview-title'>Source</div>
      <a
        href={url}
        className='d-block link-preview-value mb-3'
        style={{ cursor: 'pointer' }}
        target='_blank'
        rel='noreferrer'
      >
        Go to source<i className='icon-arrow-right'></i>
      </a>
      <div className='link-preview-title'>Annotation</div>
      <div className='link-preview-value mb-3'>
        {!annotation ? <div>No annotation</div> : annotation}
      </div>
    </>
  );
}
