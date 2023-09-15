#!/usr/bin/env python3
"""
Session authentication class
"""
from .auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """
    seession class for storing information about a user
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        create a session for the current user
        """
        try:
            assert user_id is not None
            assert isinstance(user_id, str)
        except AssertionError:
            return None
        
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
    
    def user_id_for_session_id(self, session_id: str = None) -> str:
        """"
        return a user id base on the session_id
        """
        try:
            assert session_id is not None
            assert isinstance(session_id, str)
        except AssertionError:
            return None
        
        return self.user_id_by_session_id.get(session_id, None)
    

    def current_user(self, request=None):
        """
        retrieve the current user
        """
        session_id = self.session_cookie(request)

        if session_id is not None:
            user_id = self.user_id_for_session_id(session_id)
            if user_id is not None:
                current_user = User.get(user_id)
                return current_user
            else:
                return None
        return None
    

    def destroy_session(self, request=None):
        """
        delete the user session and logout the user
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        if self.user_id_for_session_id(session_id) is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True







    