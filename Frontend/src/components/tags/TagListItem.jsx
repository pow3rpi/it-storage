export default function TagListItem(props) {
  const { tag, onMouseDown, value, isFound } = props;
  const curLength = value.length;
  const start_index = tag.indexOf(value);
  const end_index = start_index + curLength;

  return (
    <div className='tag-list-item' onMouseDown={onMouseDown}>
      {curLength > 2 && isFound ? (
        <span>
          {start_index !== 0 ? tag.slice(0, start_index) : ''}
          <b>{tag.slice(start_index, end_index)}</b>
          {end_index !== tag.length ? tag.slice(end_index) : ''}
        </span>
      ) : (
        <span>{tag}</span>
      )}
    </div>
  );
}
