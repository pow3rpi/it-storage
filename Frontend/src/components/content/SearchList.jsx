import '../../css/components/search.css';

import LinkSearchItem from './LinkSearchItem';
import TutorialSearchItem from './TutorialSearchItem';
import { ContentType } from '../../js/enum/content';

export default function SearchList(props) {
  const {
    posts,
    total,
    isDeleteMode = false,
    postsToDelete = [],
    setPostsToDelete = Function.prototype,
  } = props;

  function numberWithCommas(x) {
    x = x.toString();
    return x.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ',');
  }

  return (
    <div className='mb-3'>
      <div className='search-results d-flex justify-content-end mb-1'>
        Results: {numberWithCommas(total)}
      </div>
      {posts.map((post) => {
        let item;
        switch (post.type) {
          case ContentType.link:
            item = (
              <LinkSearchItem
                key={post.id}
                {...post}
                isDeleteMode={isDeleteMode}
                postsToDelete={postsToDelete}
                setPostsToDelete={setPostsToDelete}
              />
            );
            break;
          case ContentType.tutorial:
            item = (
              <TutorialSearchItem
                key={post.id}
                {...post}
                isDeleteMode={isDeleteMode}
                postsToDelete={postsToDelete}
                setPostsToDelete={setPostsToDelete}
              />
            );
            break;
          default:
            break;
        }
        return item;
      })}
    </div>
  );
}
