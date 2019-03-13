LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE    := base91
LOCAL_SRC_FILES := base91.cpp

include $(BUILD_SHARED_LIBRARY)
