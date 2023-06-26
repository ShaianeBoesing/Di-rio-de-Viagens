from typing import List
from Model.Comment import Comment


class CommentController:
    def __init__(self, trip_controller):
       self.__table_name = 'comments'
	   #precisa se comunicar com o trip controller
       self.__trip_controller = trip_controller

    def create_comment(self, description: str, spot_id) -> Comment:
       new_comment = Comment(description, spot_id)
       comment = new_comment.save()
       return comment
	
    def get_comment(self, comment_id: int) -> Comment:
       comment = Comment.show(comment_id)
       return {
			'id': comment.id,
			'description': comment.description,
			'date': comment.date
		}
	
    def update_comment(self, comment_id: int, **kwargs) -> None:
        print(kwargs)
        comment = Comment.show(comment_id)
        if comment:
          comment.update(**kwargs)
	
    def delete_comment(self, comment_id: int) -> None:
      comment = Comment.show(comment_id)
      if comment:
        comment.delete()
	
    def list_comments_by_spot(self, spot_id=None):
        if spot_id is None:
          return []
		
        results = Comment.list_by_spot(spot_id)
        comments = []
        for result in results:
            comment = {'description': result.description, 'id': result.id}
            comments.append(comment)
		
        return comments

    @property
    def trip_controller(self):
       return self.__trip_controller
