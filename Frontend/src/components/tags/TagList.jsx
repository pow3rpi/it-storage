import TagListItem from './TagListItem';
import { defaultTags } from '../../data/defaultTags';

export default function TagList(props) {
  const {
    suggestedTags,
    setSuggestedTags,
    tagListId,
    addTag,
    inputId,
    value,
    setValue,
    isFound,
    isSearching,
  } = props;

  let tagList = suggestedTags.map((tag, index) => (
    <TagListItem
      key={index}
      tag={tag}
      value={value}
      isFound={isFound}
      onMouseDown={() => {
        const inpuField = document.getElementById(inputId);
        inpuField.value = '';
        setValue('');
        addTag(tag);
        inpuField.blur();
        setSuggestedTags(defaultTags);
      }}
    />
  ));

  return (
    <div id={tagListId} className='d-none col-11 tags-list mt-1'>
      {isSearching ? (
        <div style={{ padding: '7px 10px', color: 'rgba(0, 0, 0, 0.55)' }}>
          Searching...
        </div>
      ) : (
        tagList
      )}
    </div>
  );
}
